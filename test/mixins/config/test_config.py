import unittest

from contrib.pyas.src.pyas_v3 import As

from src.mixins.config.config import Config


class TestConfig(unittest.TestCase):

    def test_value(self):

        config = {
            'value': 'config1 text',
            'error': 'config1 error',
            'spec': {
                'specType': 'ValueSpec',
                'label': 'config1 label',
            }
        }

        configee = As(Config)(config)

        self.assertEquals('config1 text', configee['value'])
        self.assertEquals(([],), configee.allConfigPaths)
        self.assertEquals('config1 text', configee.pick([]))

        specee = configee.specee
        self.assertEquals('ValueSpec', specee['specType'])
        self.assertEquals('config1 label', specee['label'])
        self.assertEquals('config1 error', configee['error'])

        isValid = configee.evaluate()
        self.assertTrue(isValid)
        self.assertEquals(None, configee['error'])

    def test_category(self):

        config = {
            'value': 'config1 value1',
            'error': 'config1 error',

            'spec': {
                'specType': 'CategorySpec',
                'label': 'config1 label',
                'required': True,
                'valueMetas': [
                    {'value': 'config1 value1', 'label': 'config1 label'},
                    {'value': 'config1 value2', 'label': 'config2 label'},
                ],
            }
        }

        configee = As(Config)(config)

        self.assertEquals('config1 value1', configee['value'])
        self.assertEquals('config1 error', configee['error'])
        self.assertEquals(([],), configee.allConfigPaths)
        self.assertEquals('config1 value1', configee.pick([]))

        specee = configee.specee
        self.assertEquals('CategorySpec', specee['specType'])
        self.assertEquals('config1 label', specee['label'])

        isValid = configee.evaluate()
        self.assertTrue(isValid)
        self.assertEquals(None, configee['error'])

        configee['value'] = 'non valid value'
        isValid = configee.evaluate()
        self.assertFalse(isValid)
        self.assertEquals(
            'non valid value must be one of [\'config1 value1\', \'config1 value2\'].', configee['error'])

    def test_configMap(self):

        config = {
            'spec': {
                'specType': 'ConfigMapSpec',
                'minCount': 4,
                'maxCount': 2,
                'label': 'ConfigMap label',
            },
            'error': 'ConfigMap error',
            'value': {
                'config1 key': {
                    'value': 'config1 text',
                    'error': 'config1 error',
                    'spec': {
                        'specType': 'ValueSpec',
                        'label': 'config1 label',
                    },
                },
                'config2 key': {
                    'value': 'config2 text',
                    'error': 'config2 error',
                    'spec': {
                        'specType': 'ValueSpec',
                        'label': 'config2 label',
                    },
                },
                'config3 key': {
                    'value': 'config3 text',
                    'error': 'config3 error',
                    'spec': {
                        'specType': 'ValueSpec',
                        'label': 'config3 label',
                    },
                },
            },
        }

        configee1 = As(Config)(config)
        specee1 = configee1.specee

        self.assertEquals('ConfigMapSpec', specee1['specType'])
        self.assertEquals('ConfigMap label', specee1['label'])
        self.assertEquals('ConfigMap error', configee1['error'])
        self.assertEquals((['config1 key'], ['config2 key'],
                          ['config3 key']), configee1.allConfigPaths)
        self.assertEquals('config1 text', configee1.pick(('config1 key',),))
        self.assertEquals('config2 text', configee1.pick(('config2 key',),))
        self.assertEquals('config3 text', configee1.pick(('config3 key',),))
        self.assertIsNone(configee1.pick(['config4 key'],))

        configee11 = As(Config)(configee1['value']['config1 key'])
        specee11 = configee11.specee

        self.assertEquals('ValueSpec', specee11['specType'])
        self.assertEquals('config1 label', specee11['label'])
        self.assertEquals('config1 error', configee11['error'])

        configee12 = As(Config)(configee1['value']['config2 key'])
        specee12 = configee12.specee

        self.assertEquals('ValueSpec', specee12['specType'])
        self.assertEquals('config2 label', specee12['label'])
        self.assertEquals('config2 error', configee12['error'])

        isValid = configee1.evaluate()
        self.assertEquals(
            'ConfigMap label must have at least 4 values.', configee1['error'])
        self.assertFalse(isValid)
        config['spec']['minCount'] = 1

        isValid = configee1.evaluate()
        self.assertEquals(
            'ConfigMap label must have at most 2 values.', configee1['error'])
        self.assertFalse(isValid)
        config['spec']['maxCount'] = 4

        isValid = configee1.evaluate()
        self.assertEquals(
            None, configee1['error'])
        self.assertTrue(isValid)
        self.assertEquals('config1 text', configee1.pick(('config1 key',)))
        self.assertEquals('config2 text', configee1.pick(('config2 key',)))
        self.assertEquals('config3 text', configee1.pick(('config3 key',)))

    def test_required(self):

        config = {
            'spec': {
                'specType': 'ConfigMapSpec',
            },
            'error': None,
            'value': {
                'config1': {
                    'value': None,
                    'error': 'config1 error',
                    'spec': {
                        'specType': 'ValueSpec',
                        'label': 'config1 label',
                        'required': True
                    }
                },
                'config2': {
                    'value': None,
                    'error': 'config2 error',
                    'spec': {
                        'specType': 'CategorySpec',
                        'label': 'config2 label',
                        'required': True,
                        'valueMetas': [
                            {
                                'value': None,
                                'label': 'None',
                            },
                            {
                                'value': 'cat_1',
                                'label': 'cateqgory 1',
                            },
                        ]
                    },
                }
            }
        }

        configee = As(Config)(config)
        specee = configee.specee

        config['value']['config1']['spec']['required'] = False
        config['value']['config2']['spec']['required'] = False

        isValid = configee.evaluate()
        self.assertTrue(isValid)

        config['value']['config1']['spec']['required'] = True
        isValid = configee.evaluate()
        self.assertFalse(isValid)
        self.assertEquals('config1 label is required.',
                          config['value']['config1']['error'])

        config['value']['config1']['value'] = 'as required'
        isValid = configee.evaluate()
        self.assertTrue(isValid)
        self.assertEquals(None, config['value']['config1']['error'])

        config['value']['config2']['spec']['required'] = True
        isValid = configee.evaluate()
        self.assertFalse(isValid)
        self.assertEquals('config2 label is required.',
                          config['value']['config2']['error'])

        config['value']['config2']['value'] = 'cat_1'
        isValid = configee.evaluate()
        self.assertTrue(isValid)
        self.assertEquals(None, config['value']['config2']['error'])

    def test_allowedTypes(self):

        config = {
            'label': 'config1 label',
            'value': 'config1 text',
            'error': 'config1 error',
            'spec': {
                'specType': 'ValueSpec',
            }
        }

        configee = As(Config)(config)
        specee = configee.specee

        self.assertEquals(None, configee['allowedTypes'])

        specee['allowedTypes'] = [str]
        self.assertEquals([str], specee['allowedTypes'])
        isValid = configee.evaluate()
        self.assertTrue(isValid)
        self.assertEquals([str()], config['spec']['allowedTypes'])
        self.assertEquals(None, configee['error'])

        specee['allowedTypes'] = [float]
        self.assertEquals([float], specee['allowedTypes'])
        isValid = configee.evaluate()
        self.assertFalse(isValid)
        self.assertEquals([float()], config['spec']['allowedTypes'])
        self.assertEquals(
            "config1 text must be of type [<class 'float'>].", configee['error'])

        specee['allowedTypes'] = [str()]
        self.assertEquals([str], specee['allowedTypes'])
        isValid = configee.evaluate()
        self.assertTrue(isValid)
        self.assertEquals([str()], config['spec']['allowedTypes'])
        self.assertEquals(None, configee['error'])


if __name__ == '__main__':

    unittest.main()
