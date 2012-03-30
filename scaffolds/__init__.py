from pyramid.scaffolds import PyramidTemplate

class ZODBUsersTemplate(PyramidTemplate):
    _template_dir = 'zodb_users'
    summary = 'Creates pyramid project with simple user management'

class SimpleBaseTemplate(PyramidTemplate):
    _template_dir = 'simple_base'
    summary = 'Creates pyramid project with base that contains translation functionality, \
            twitter bootstrap and simple page model'
