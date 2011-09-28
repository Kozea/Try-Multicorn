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



TABLE_TYPES = {
    'LDAP': TableType('LDAP', wrapper='multicorn.ldapfdw.LdapFdw',
        required_options=('address', 'path', 'objectclass'),
        allowed_columns=('sn', 'cn', 'uid', 'uidNumber', 'o', 'mail'),
        info=u"An access point for ldap."),
    'RSS': TableType('RSS', wrapper='multicorn.rssfdw.RssFdw',
        required_options=('url',),
        allowed_columns=(
            'title',
            'link',
            'guid',
            'pubDate',
            'description'))
}
