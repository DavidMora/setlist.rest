import unittest
from modules.helpers.modules import extractAndRemoveModules, validateModuleCompleteness

class Object(object):
    pass

class TestModules(unittest.TestCase):
    def setUp(self):
        self.kwargs = {
            'modules': {
                'daw': 'Cubase',
                'songs': 'Rock',
                'setlist': 'March 2023'
            },
            'param1': 'value1',
            'param2': 'value2'
        }

    def test_extractAndRemoveModules(self):
        extracted = extractAndRemoveModules(self.kwargs)
        self.assertDictEqual(extracted, {'modules': {'daw': 'Cubase', 'songs': 'Rock', 'setlist': 'March 2023'}, 'kwargs': {'param1': 'value1', 'param2': 'value2'}})
        self.assertDictEqual(self.kwargs, {'modules': {'daw': 'Cubase', 'songs': 'Rock', 'setlist': 'March 2023'}, 'param1': 'value1', 'param2': 'value2'})

    def test_validateModuleCompleteness(self):
        obj = Object()
        obj.modules = {'modules': {'daw': None, 'songs': 'Rock', 'setlist': 'March 2023'}}
        self.assertRaises(Exception, validateModuleCompleteness, obj)
        obj.modules = {'modules': {'daw': 'Cubase', 'songs': None, 'setlist': 'March 2023'}}
        self.assertRaises(Exception, validateModuleCompleteness, obj)
        obj.modules = {'modules': {'daw': 'Cubase', 'songs': 'Rock', 'setlist': None}}
        self.assertRaises(Exception, validateModuleCompleteness, obj)
        obj.modules = {'daw': 'Cubase', 'songs': 'Rock', 'setlist': 'March 2023'}
        self.assertIsNone(validateModuleCompleteness(obj))

if __name__ == '__main__':
    unittest.main()
