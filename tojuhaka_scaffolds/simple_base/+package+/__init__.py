from pyramid.config import Configurator
from pyramid_zodbconn import get_connection
from .models import appmaker

def root_factory(request):
    conn = get_connection(request)
    return appmaker(conn.root())

def my_locale_negotiator(request):
    try:
        locale_name = request.cookies['lang']
    except KeyError:
        locale_name = u'en'
    return locale_name

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory=root_factory, settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_translation_dirs('locale/')
    config.set_locale_negotiator(my_locale_negotiator)
    config.scan()
    return config.make_wsgi_app()
