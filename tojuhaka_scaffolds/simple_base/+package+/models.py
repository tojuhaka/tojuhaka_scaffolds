from persistent.mapping import PersistentMapping
from persistent import Persistent

from .interfaces import IContent, IPage, IContainer
from .interfaces import IPages, ISiteRoot
from zope.interface import implements

class Main(PersistentMapping):
    implements(ISiteRoot)
    __parent__ = __name__ = None

class Page(Persistent):
    implements(IContent, IPage)

    def __init__(self, name):
        Persistent.__init__(self)
        self.__name__ = name
        self.id = name
        self.name = name

class Pages(PersistentMapping):
    implements(IContainer, IPages)

    def __init__(self, name):
        PersistentMapping.__init__(self)
        self.__name__ = name
        self.id = name
        self.name = name

    def add(self, id):
        page = Page(id)
        page.__parent__ = self
        self[id] = page
    
    def remove(self, id):
        self.pop(id)


def appmaker(zodb_root):
    if not 'main' in zodb_root:
        app_root = Main()

        pages = Pages('pages')
        pages.__parent__ = app_root

        pages.add('contact')
        app_root['pages'] = pages
        zodb_root['main'] = app_root
        
        import transaction
        transaction.commit()
    return zodb_root['main']
