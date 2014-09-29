import pkg_resources

from .resolver import DependencyTable
from .version import PYDEPEND_VERSION


class PluginError(Exception):
    '''
    Raised for plugin-related errors.
    '''


class Context(object):
    '''
    Plugin run and install context.
    '''

    __defaults = None
    __options = None
    __plugins = None
    __registry = None

    def __init__(self, defaults=()):
        self.__defaults = dict(defaults)
        self.__options = {}
        self.__plugins = []
        self.__registry = {}

    @property
    def plugins(self):
        return tuple(self.__plugins)

    @property
    def options(self):
        res = dict(self.__defaults)
        res.update(self.__options)

        return res

    def set_option(self, name, value):
        if name in self.__options:
            raise PluginError('Option {!r} already set'.format(name))

        self.__options[name] = value

    def add_plugin(self, plugin):
        if not isinstance(plugin, Plugin):
            raise PluginError("Unknown plugin object type {}".format(type(plugin).__name__))

        self.__plugins.append(plugin)

    def register(self, name, obj):
        if hasattr(self, name):
            raise AttributeError('Attribute {!r} already exists'.format(name))

        self.__registry[name] = obj

    def __getattr__(self, name):
        if name not in self.__registry:
            raise AttributeError(name)

        return self.__registry[name]


class Plugin(object):
    '''
    A plugin is an extension of the pydepend application.
    '''

    name = None

    def get_name(self):
        '''
        Get the plugin name.
        '''

        return self.name or type(self).__name__

    def setup_cli_options(self, parser):
        '''
        Setup the plugin command line options.
        '''

    def setup(self, context):
        '''
        Setup the plugin. If the function returns True, the plugin
        is enabled, if it returns False, it is disabled.
        '''

        return True

    def install(self, context):
        '''
        Install the plugin.
        '''

        raise NotImplementedError('{}.install'.format(type(self).__name__))

    def get_requires(self):
        '''
        Return the list of plugin names required for loading this plugin.
        '''

        return ()


class PluginSource(object):
    '''
    Manage pydepend plugin sources.
    '''

    def load_plugins(self):
        '''
        Iterate through all plugins.
        '''

        raise NotImplementedError('{}.load_plugins'.format(type(self).__name__))


class EntryPointSource(PluginSource):
    '''
    Plugin source that iterates through the given entry points.
    '''

    def __init__(self, name, iter_func=None):
        self.__name = name
        self.__iter_func = iter_func or pkg_resources.iter_entry_points

    def load_plugins(self):
        for ep in self.__iter_func(self.__name):
            yield ep.load()


class DirectPluginSource(PluginSource):
    '''
    Returns directly a list of plugins.
    '''

    def __init__(self, plugins):
        self.__plugins = list(plugins)

    def load_plugins(self):
        return iter(self.__plugins)


class CompositePluginSource(PluginSource):
    '''
    Plugin source combining several other plugin sources.
    '''

    def __init__(self, sources):
        self.__sources = list(sources)

    def load_plugins(self):
        for source in self.__sources:
            for plugin in source.load_plugins():
                yield plugin


class DefaultPluginSource(CompositePluginSource):
    '''
    Default plugin source
    '''

    def __init__(self):
        from .ext import BUILTIN_MODULES

        super(DefaultPluginSource, self).__init__(
            [
                EntryPointSource('pydepend.{}'.format(PYDEPEND_VERSION.major)),
                EntryPointSource('pydepend.{}.{}'.format(PYDEPEND_VERSION.major, PYDEPEND_VERSION.minor)),
                DirectPluginSource(BUILTIN_MODULES),
            ]
        )


class PluginManager(object):
    '''
    Manage plugins loaded from different sources.
    '''

    def __init__(self, plugin_source=None):
        if plugin_source is None:
            plugin_source = DirectPluginSource()

        plugins = {plugin.get_name(): plugin for plugin in plugin_source.load_plugins()}
        load_order = DependencyTable(
            (name, plugin.get_requires()) for name, plugin in plugins.items()
        ).resolve_all(flat=True)

        self.__plugins = [plugins[name] for name in load_order]

    def install(self, context, plugins):
        '''
        Install all plugins.
        '''

        plugins = set(plugins)

        for plugin in self.__plugins:
            if plugin.get_name() not in plugins:
                continue

            context.add_plugin(plugin)
            plugin.install(context)

    def setup_cli_options(self, parser):
        '''
        Setup command line interface options.
        '''

        for plugin in self.__plugins:
            plugin.setup_cli_options(parser)

    def setup(self, context):
        '''
        Setup plugins. This will return the list of enabled plugins.
        '''

        passed = []

        for plugin in self.__plugins:
            if any(requirement not in passed for requirement in plugin.get_requires()):
                continue

            should_install = plugin.setup(context)
            if should_install:
                passed.append(plugin.get_name())

        return passed
