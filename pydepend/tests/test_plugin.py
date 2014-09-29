import argparse
import unittest
import shlex

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

    def test_register(self):
        self.obj = object()
        self.context.register('testobj', self.obj)

        self.assertEqual(self.obj, self.context.testobj)

    def test_register_builtin(self):
        self.assertRaises(AttributeError, self.context.register, 'plugins', object())

    def test_register_double(self):
        self.context.register('testobj', object())

        self.assertRaises(AttributeError, self.context.register, 'testobj', object())


class TestPlugin(unittest.TestCase):
    def test_get_name(self):
        self.assertEqual('ExamplePlugin', ExamplePlugin().get_name())
        self.assertEqual('name', ExamplePlugin(name='name').get_name())


class TestPluginManager(unittest.TestCase):
    def install(self, plugins, context=None, install_list=None):
        source = ExamplePluginSource(plugins)
        manager = PluginManager(source)

        if context is None:
            context = Context()

        if install_list is None:
            install_list = [plugin.get_name() for plugin in plugins]

        manager.install(context, install_list)

        return context

    def setup_cli_options(self, plugins, cli):
        source = ExamplePluginSource(plugins)
        manager = PluginManager(source)
        parser = argparse.ArgumentParser()

        manager.setup_cli_options(parser)

        return parser.parse_args(shlex.split(cli))

    def setup(self, plugins, context=None):
        source = ExamplePluginSource(plugins)
        manager = PluginManager(source)

        return manager.setup(context or Context())

    def test_install(self):
        context = self.install(
            [ExamplePlugin(option='test-run-completed')], 
            Context({'test-run-completed': False})
        )

        self.assertEqual(1, len(context.plugins))
        self.assertEqual(ExamplePlugin, type(context.plugins[0]))
        self.assertTrue(context.options['test-run-completed'])

    def test_install_with_dependencies(self):
        context = self.install(
            (
                ExamplePlugin(name='plugin1', requires=('plugin0',)),
                ExamplePlugin(option='plugin-option', name='plugin0'),
            )
        )

        self.assertListEqual(
            ['plugin0', 'plugin1'],
            list(plugin.get_name() for plugin in context.plugins)
        )

    def test_install_limited(self):
        context = self.install(
            (
                ExamplePlugin(name='plugin1', requires=('plugin0',)),
                ExamplePlugin(option='plugin-option', name='plugin0'),
            ),
            install_list=('plugin0',)
        )

        self.assertListEqual(
            ['plugin0'],
            list(plugin.get_name() for plugin in context.plugins)
        )

    def test_setup_cli_options(self):
        options = self.setup_cli_options(
            [ExamplePlugin(name='plugin')],
            '--option 1'
        )

        self.assertEqual(1, options.option)

    def test_setup(self):
        context = Context()
        context.set_option('option', 2)

        install = self.setup([ExamplePlugin(name='plugin')], context)

        self.assertListEqual(['plugin'], install)
        self.assertTrue(context.options['plugin-setup'])

    def test_setup_non_installed(self):
        install = self.setup(
            [
                ExamplePlugin(name='plugin0'),
                ExamplePlugin(name='plugin1', install=False),
            ]
        )

        self.assertListEqual(['plugin0'], install)

    def test_setup_ignores_unmet_dependencies(self):
        install = self.setup(
            [
                ExamplePlugin(name='plugin0', requires=('plugin1',)),
                ExamplePlugin(name='plugin1', install=False),
            ]
        )

        self.assertListEqual([], install)


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
    def __init__(self, option='test-run-completed', name=None, requires=(), install=True):
        self.name = name
        self.requires = tuple(requires)
        self.option = option
        self.should_install = install

    def install(self, context):
        context.set_option(self.option, True)

    def get_requires(self):
        return self.requires

    def setup_cli_options(self, parser):
        parser.add_argument('--option', type=int)

    def setup(self, context):
        context.set_option('{}-setup'.format(self.get_name()), True)
        return self.should_install


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
