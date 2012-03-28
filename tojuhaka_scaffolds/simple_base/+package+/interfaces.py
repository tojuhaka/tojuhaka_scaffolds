from zope.interface import Interface
from zope.interface import Attribute

class ISiteRoot(Interface):
    """ Mark the object as root """

class IContent(Interface):
    """ Single object which is inside container"""
    name = Attribute("""Name of the content""")
    id = Attribute("""ID of the page. Could be the \
            same as the name""")

class IContainer(Interface):
    """ Contains objects """
    def add(obj_name):
        """ Add a single object """
    def remove(obj_id):
        """ Remove object by id """

class IPage(Interface):
    """ Mark the object as page """

class IPages(Interface):
    """ Mark the object as pages  """
