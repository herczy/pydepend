import pkg_resources

from .resolver import DependencyTable
from .version import PYDEPEND_VERSION
from .ext import BUILTIN_MODULES


class PluginError(Exception):
    '''
    Raised for plugin-related errors.
    '''


class Context(object):
    '''
    Plugin run and install context.
    '''

    def __init__(self, defaults=()):
        self.__defaults = dict(defaults)
        self.__options = {}
        self.__plugins = []

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

    __sources = [
        EntryPointSource('pydepend.{}'.format(PYDEPEND_VERSION.major)),
        EntryPointSource('pydepend.{}.{}'.format(PYDEPEND_VERSION.major, PYDEPEND_VERSION.minor)),
        DirectPluginSource(BUILTIN_MODULES),
    ]

    def __init__(self):
        super(DefaultPluginSource, self).__init__(self.__sources)


class PluginManager(object):
    '''
    Manage plugins loaded from different sources.
    '''

    def __init__(self, plugin_source=None):
        self.__plugin_source = plugin_source or DirectPluginSource()

    def install(self, context):
        '''
        Install all plugins.
        '''

        plugins = {plugin.get_name(): plugin for plugin in self.__plugin_source.load_plugins()}

        load_order = DependencyTable(
            (name, plugin.get_requires()) for name, plugin in plugins.items()
        ).resolve_all(flat=True)

        for plugin_name in load_order:
            plugin = plugins[plugin_name]
            context.add_plugin(plugin)
            plugin.install(context)
