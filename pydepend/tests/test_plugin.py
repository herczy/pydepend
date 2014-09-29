import unittest

from ..plugin import Context, PluginSource, Plugin, PluginError, PluginManager, EntryPointSource, \
    CompositePluginSource, DirectPluginSource


class TestContext(unittest.TestCase):
    def setUp(self):
        self.defaults = {'default-value': 1}
        self.context = Context(self.defaults)

    def test_options(self):
        self.context.set_option('option', 'value')

        self.assertDictEqual(
            {
                'option': 'value',
                'default-value': 1,
            },
            self.context.options
        )

    def test_set_something_twice(self):
        self.context.set_option('twice', 1)

        self.assertRaises(PluginError, self.context.set_option, 'twice', 2)

    def test_add_plugin_non_plugin_object(self):
        self.assertRaises(PluginError, self.context.add_plugin, object())

    def test_add_plugin(self):
        self.context.add_plugin(ExamplePlugin())

        self.assertEqual(1, len(self.context.plugins))
        self.assertEqual(ExamplePlugin, type(self.context.plugins[0]))


class TestPlugin(unittest.TestCase):
    def test_get_name(self):
        self.assertEqual('ExamplePlugin', ExamplePlugin().get_name())
        self.assertEqual('name', ExamplePlugin(name='name').get_name())


class TestPluginManager(unittest.TestCase):
    def setUp(self):
        self.source = ExamplePluginSource()
        self.manager = PluginManager(self.source)

    def test_install(self):
        context = Context({'test-run-completed': False})
        self.source.plugins.append(ExamplePlugin(option='test-run-completed'))

        self.manager.install(context)

        self.assertEqual(1, len(context.plugins))
        self.assertEqual(ExamplePlugin, type(context.plugins[0]))
        self.assertTrue(context.options['test-run-completed'])

    def test_install_with_dependencies(self):
        context = Context()
        self.source.plugins.extend(
            (

                ExamplePlugin(name='plugin1', requires=('plugin0',)),
                ExamplePlugin(option='plugin-option', name='plugin0'),
            )
        )

        self.manager.install(context)

        self.assertListEqual(
            ['plugin0', 'plugin1'],
            list(plugin.get_name() for plugin in context.plugins)
        )


class TestEntryPointSource(unittest.TestCase):
    def __iterate_entry_points(self, name):
        for ep in self.entry_points:
            yield FakeEntryPoint(ep)
        
    def setUp(self):
        self.entry_points = [ExamplePlugin(name='test')]
        self.source = EntryPointSource('test', iter_func=self.__iterate_entry_points)

    def test_load_plugins(self):
        self.assertListEqual(
            ['test'],
            [plugin.get_name() for plugin in self.source.load_plugins()]
        )


class TestDirectPluginSource(unittest.TestCase):
    def test_load_plugins(self):
        source = DirectPluginSource([ExamplePlugin(name='test')])

        self.assertListEqual(
            ['test'],
            [plugin.get_name() for plugin in source.load_plugins()]
        )


class TestCompositePluginSource(unittest.TestCase):
    def test_load_plugins(self):
        source = CompositePluginSource(
            [
                ExamplePluginSource([ExamplePlugin(name='plugin0')]),
                ExamplePluginSource([ExamplePlugin(name='plugin1')]),
            ]
        )

        self.assertListEqual(
            ['plugin0', 'plugin1'],
            [plugin.get_name() for plugin in source.load_plugins()]
        )


class ExamplePlugin(Plugin):
    def __init__(self, option='test-run-completed', name=None, requires=()):
        self.name = name
        self.requires = tuple(requires)
        self.option = option

    def install(self, context):
        context.set_option(self.option, True)

    def get_requires(self):
        return self.requires


class ExamplePluginSource(PluginSource):
    def __init__(self, initial_sources=()):
        self.plugins = list(initial_sources)

    def load_plugins(self):
        return tuple(self.plugins)


class FakeEntryPoint(object):
    def __init__(self, obj):
        self.__obj = obj

    def load(self):
        return self.__obj
