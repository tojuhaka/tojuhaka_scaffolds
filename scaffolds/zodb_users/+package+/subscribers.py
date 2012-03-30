from pyramid.renderers import get_renderer
from pyramid.interfaces import IBeforeRender
from pyramid.events import subscriber

from pyramid.view import render_view


class Provider(object):
    """ Provides rendered pages inside other templates """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, name='', secure=True):
        # Decode to utf8, else it's gonna throw UnicodeDecodeError
        try:
            return render_view(self.context, self.request, name, secure).decode("utf8")
        except AttributeError:
            #Handle none object
            pass
        return None


@subscriber(IBeforeRender)
def add_base_template(event):
    base = get_renderer('templates/base.pt').implementation()
    event.update({
        'base': base,
        'provider': Provider(event['context'], event['request'])
    })


