import os.path


class NotAPythonModuleError(Exception):
    pass


def _is_package(path):
    return os.path.isdir(path) and os.path.isfile(os.path.join(path, '__init__.py'))


def scan(basepath):
    for sub in os.listdir(basepath):
        full = os.path.abspath(os.path.join(basepath, sub))

        if os.path.isdir(full):
            yield full
            for res in scan(full):
                yield res

        else:
            yield full


def reduce_package_name(path):
    modpath, name = os.path.split(path)
    if not os.path.isdir(path):
        if not name.endswith('.py'):
            raise NotAPythonModuleError(path)

        name = name[:-3]

    elif not _is_package(path):
        raise NotAPythonModuleError(path)

    if not _is_package(modpath):
        return modpath, name

    modpath, pkgname = reduce_package_name(modpath)
    return modpath, pkgname + '.' + name
