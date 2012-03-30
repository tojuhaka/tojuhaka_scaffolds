from persistent.mapping import PersistentMapping
from persistent import Persistent

from .security import pwd_context, salt, acl, group_names

from datetime import datetime
from pyramid.security import Allow
from .interfaces import ISite
from zope.interface import implements


class Main(PersistentMapping):
    """ Main root object in our ZODB database """
    implements(ISite)
    """ Root object for ZODB """
    __name__ = None
    __parent__ = None
    __acl__ = acl


class Users(PersistentMapping):
    implements(ISite)
    """ Contains all the users """

    def has_user(self, username):
        if username in self.keys():
            return True
        return False

    def add(self, username, password, email):
        user = User(username, password, email)
        user.__name__ = username
        user.__parent__ = self
        self[user.username] = user


class User(Persistent):
    implements(ISite)

    @property
    def __acl__(self):
        acls = [(Allow, 'u:%s' % self.username, 'edit_user'),
                (Allow, group_names['admin'], 'edit_user')]
        return acls

    def __init__(self, username, password, email):
        self.username = username
        self.password = pwd_context.encrypt(password + salt)
        self.email = email
        self.timestamp = datetime.now()

    def edit(self, password, email):
        self.password = pwd_context.encrypt(password + salt)
        self.email = email

    def validate_password(self, password):
        return pwd_context.verify(password + salt, self.password)


class Groups(PersistentMapping):
    implements(ISite)
    """ Contains the information about the groups of
    the users """

    def add(self, username, group):
        """ Add a single group to username """
        try:
            self[username]
        except KeyError:
            self[username] = []

        if not group in self[username]:
            self[username] += [group]

    def remove_group(self, username, group):
        if group in self[username]:
            self[username].remove(group)

    def flush(self, username):
        self[username] = []

    def add_policy(self, policy):
        """ Updates the group-policy with dict that contains
        usernames and list of groups behind it. Add also the
        user-marker 'u:user' to group. We need it for __acl__
        inside class. """

        for username in policy.keys():
            self[username] = policy[username] + [u'u:%s' % username]


def appmaker(zodb_root):
    if not 'app_root' in zodb_root:
        app_root = Main()
        users = Users()
        groups = Groups()
        app_root['users'] = users
        app_root['groups'] = groups

        users.__name__ = 'users'
        users.__parent__ = app_root
        groups.__name__ = 'groups'
        groups.__parent__ = app_root

        users.add('admin', 'adminpw#', 'admin@admin.com')
        users.add('editor', 'editorpw#', 'editor@editor.com')
        users.add('member', 'memberpw#', 'member@member.com')
        groups.add('admin', group_names['admin'])
        groups.add('admin', 'u:admin')
        groups.add('editor', 'u:editor')
        groups.add('member', 'u:member')

        zodb_root['app_root'] = app_root
        import transaction
        transaction.commit()
    return zodb_root['app_root']
