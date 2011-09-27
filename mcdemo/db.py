from flaskext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.schema import DDLElement

db = SQLAlchemy()

class GrantSelect(DDLElement):

    def __init__(self, on_table, to_user):
        self.on_table = on_table
        self.to_user = to_user

@compiles(GrantSelect)
def grant_select(grant, compiler, **kw):
    preparer = compiler.dialect.identifier_preparer
    on = preparer.quote_identifier(grant.on_table)
    to = preparer.quote_identifier(grant.to_user)
    return "GRANT SELECT ON %s TO %s" % (on, to)

def get_admin_bind():
    return db.get_engine(db.get_app(), 'admin')
