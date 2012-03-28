import unittest

from .models import appmaker

from .interfaces import IContainer, IContent
from .models import Page, Pages

class AppMakerTests(unittest.TestCase):
    def test_it(self):
        root = {}
        appmaker(root)
        self.assertEqual(root['main']['pages'].__name__,
                         'pages')
        self.assertTrue(root['main'].__parent__ == None)

class ModelTests(unittest.TestCase):
    def test_interfaces(self):
        from zope.interface.verify import verifyClass
        self.assertTrue(verifyClass(IContainer, Pages))
        self.assertTrue(verifyClass(IContent, Page))
        

class FunctionalTests(unittest.TestCase):
    def setUp(self):
        # Build testing environment
        import tempfile
        import os.path
        from . import main
        self.tmpdir = tempfile.mkdtemp()

        dbpath = os.path.join(self.tmpdir, 'test.db')
        uri = 'file://' + dbpath
        settings = {'zodbconn.uri': uri,
                     'pyramid.includes': ['pyramid_zodbconn', 'pyramid_tm']}

        app = main({}, **settings)
        self.db = app.registry.zodb_database
        from webtest import TestApp
        self.testapp = TestApp(app)

    def tearDown(self):
        import shutil
        self.db.close()
        shutil.rmtree(self.tmpdir)

    def test_home_url(self):
        res = self.testapp.get('/', status=200)
        self.assertTrue(res.status == '200 OK')

