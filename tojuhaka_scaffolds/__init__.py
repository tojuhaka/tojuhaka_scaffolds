from pyramid.scaffolds import PyramidTemplate


class ZODBUsersTemplate(PyramidTemplate):
    _template_dir = 'zodb_users'
    summary = 'Creates pyramid project with user management'
