
import logging
import unittest


logging.basicConfig(
    level=logging.INFO,
    filename='test.log',
    datefmt="%Y-%m-%d %H:%M:%S",
    format = "【%(asctime)s %(levelname)s】 %(lineno)d: %(message)s"
)

class UserDict(dict):
    def __init__(self,**kw):
        super().__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"Dict object has no attribute '%s'"%key)

    def __setattr__(self, key, value):
        self[key] = value



class TestUserDict(unittest.TestCase):

    def setUp(self):
        logging.info('SetUp...')

    def test_init(self):
        d = UserDict(a=1,b='test')
        self.assertEqual(d.a,1)
        self.assertEqual(d.b,'test')
        self.assertTrue(isinstance(d,dict))

    def test_key(self):
        d = UserDict()
        d['key'] = 'value'
        self.assertEqual(d.key,'value')

    def test_attr(self):
        d = UserDict()
        d.key = 'value'
        self.assertTrue('key' in d)
        self.assertEqual(d['key'],'value')

    def test_keyerror(self):
        d = UserDict()
        with self.assertRaises(KeyError):
            value = d['empty']

    def test_attrerror(self):
        d = UserDict()
        with self.assertRaises(AttributeError):
            value = d.empty


    def tearDown(self):
        logging.info('tearDown')


if __name__ == '__main__':
    unittest.main()