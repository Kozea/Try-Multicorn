# -*- coding: utf-8 -*-
from flask import render_template, Response, jsonify
from flask import request
from mcdemo.db import db, get_admin_bind, GrantSelect
from sqlalchemy.exc import ProgrammingError
from sqlalchemy_fdw import ForeignTable
from sqlalchemy import Column, MetaData
from sqlalchemy.sql import text

import json
import datetime
from itertools import islice, izip_longest, izip
from .tabletypes import TABLE_TYPES, TYPES

class Encoder(json.JSONEncoder):
    """Encoder used for dumping database's values"""

    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        return super(Encoder, self).default(obj)


def format_table(result):
    """Format an sqlalchmey rowresult proxy to a list of lines.

    The elements are json-encoded, and each line has the same length

    ex:

        substr  |         link         |   pubDate
    -------------------------------------------------
    "Off to a " | "http://example.com" | "2011-09-26"
    "How to ma" | "http://example.com" | "2011-09-26"
    "Don't jud" | "http://example.com" | "2011-09-26"

    """
    colslength = []
    # Dump everything to json strings
    result = [result.keys()] + [[unicode(json.dumps(item, cls=Encoder))
                for item in line]
                for line in  islice(result, 0, 50)]
    # Compute line length
    lines = len(result) - 1
    for line in result:
        colslength = [max(len(item), length)
                for item, length in izip_longest(line, colslength, fillvalue=0)]
    # Caution: the spaces are replaced by non breaking spaces
    result = (u' | '.join([item.center(length).replace(u' ', u' ')
                for item, length in izip(line, colslength)])
                for line in result)
    yield next(result)
    # Add 3 characters for each columns separation, minus 3 because we
    # don't need one for the last column.
    yield u'-' * ( sum((length + 3 for length in colslength)) -3)
    for line in result:
        yield line
    yield u"( %d lines )" % lines


def register(app):
    FDW_SERVER = app.config['DB_FDW_SERVER']
    metadata = MetaData()

    @app.route('/')
    def index():
        return render_template('index.html', table_types=TABLE_TYPES,
                column_types=TYPES.keys())

    @app.route('/js/multicorn.js')
    def multicornjs():
        js = render_template('multicorn.js')
        return Response(js, mimetype="application/x-javascript")

    @app.route('/query/', methods=('post',))
    def send_query():
        try:
            result = db.session.bind.execute(text(request.values.get('query')));
        except ProgrammingError as e:
            return jsonify({'result': e.message})
        table = [{'msg': line} for line in format_table(result)]
        return jsonify({'result': table})

    @app.route('/tables/add', methods=('post',))
    def add_table():
        definition = json.loads(request.data)
        columns = [Column(column['name'], TYPES[column['type']])
                for column in definition['columns']]
        table_type = TABLE_TYPES[definition['table_type']]
        if definition['name'] in metadata.tables:
            return jsonify({'error': 'The table already exists!'})
        for option in definition['options']:
            assert option in (table_type.required_options + table_type.allowed_options)
        definition['options']['wrapper'] = table_type.wrapper
        table = ForeignTable(definition['name'], metadata, *columns, fdw_server=FDW_SERVER,
                fdw_options=definition['options'])
        if table.exists(bind=get_admin_bind()):
            return jsonify({'error': 'The table already exists!'})
        table.create(bind=get_admin_bind())
        GrantSelect(definition['name'], 'multicorn').execute(get_admin_bind())
        return jsonify({'hugesuccess': True})
