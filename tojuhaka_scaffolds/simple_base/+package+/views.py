from pyramid.view import view_config
from .models import Main

class BaseView(object):
    """ Base view for everything. Defines some
    basic attributes and functions that are used
    in every view """
    def __init__(self, context, request):
        self.context = context
        self.request = request

        from pyramid.renderers import get_renderer
        base = get_renderer('templates/base.pt').implementation()

        self.base_dict = {
            'base': base,
        }


class MainView(BaseView):
    @view_config(context=Main, renderer='templates/index.pt')
    def __call__(self):
        return dict(self.base_dict.items())
