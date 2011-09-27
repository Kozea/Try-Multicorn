from mcdemo.db import db

TYPES = {
        'Unicode': db.Unicode,
        'Integer': db.Integer,
        'Numeric': db.Numeric,
        'DateTime': db.DateTime,
        'Date': db.Date
}

ANY_TYPE = tuple(TYPES.values())

class TableType(object):

    def __init__(self, name, wrapper, required_options=(), allowed_options=(),
            allowed_columns=(), info=""):
        self.name = name
        self.wrapper = wrapper
        self.required_options = required_options
        self.allowed_options = allowed_options
        self.allowed_columns = allowed_columns
        self.info = info

class ColumnDefinition(object):

    def __init__(self, name=None, allowed_types=ANY_TYPE, info=""):
        self.name = name
        self.allowed_types = allowed_types
        self.info = info


TABLE_TYPES = {
    'LDAP': TableType('LDAP', wrapper='multicorn.ldapfdw.LdapFdw',
        required_options=('address', 'path', 'objectclass'),
        allowed_columns=None,
        info=u"An access point for ldap."),
    'RSS': TableType('RSS', wrapper='multicorn.rssfdw.RssFdw',
        required_options=('url',),
        allowed_columns=(
            ColumnDefinition('title', (db.Unicode,)),
            ColumnDefinition('link', (db.Unicode,)),
            ColumnDefinition('guid', (db.Unicode,)),
            ColumnDefinition('pubDate', (db.Unicode, db.DateTime, db.Date)),
            ColumnDefinition('description', (db.Unicode,))))
}
