class DependencyError(Exception):
    '''
    Dependency resolution error base class.
    '''


class CircularDependencyError(DependencyError):
    '''
    Raised when circular dependencies are detected.
    '''


class UnknownDependencyError(DependencyError):
    '''
    Raised when unknown dependencies are detected.
    '''


class DependencyTable(object):
    def __init__(self, table=()):
        self.__table = dict(table)
        self.__verify_no_unknown_dependencies()
        self.__verify_no_circular_dependencies()
        self.__ordering = self.__get_total_ordering()

    def resolve_all(self, *args, **kwargs):
        return self.resolve(self.__table.keys(), *args, **kwargs)

    def resolve(self, names, flat=False):
        unknown = [name for name in names if name not in self.__table]
        if unknown:
            raise UnknownDependencyError('Unknown plugins: {}'.format(', '.join(unknown)))

        resolve = set(self.__get_all_dependencies(names))

        if flat:
            return [value for level in self.__ordering for value in level.intersection(resolve)]

        levels = [level.intersection(resolve) for level in self.__ordering]
        return [level for level in levels if level]

    def __get_all_dependencies(self, names):
        stack = list(names)

        while stack:
            top = stack.pop()
            stack.extend(self.__table[top])

            yield top

    def __get_total_ordering(self):
        remainder = set(self.__table.keys())
        ordering = []
        allowed = set()

        while remainder:
            paralell_deps = set(self.__resolve_given_order(remainder, allowed))
            assert paralell_deps

            remainder -= paralell_deps

            ordering.append(paralell_deps)
            allowed.update(paralell_deps)

        return ordering

    def __resolve_given_order(self, base, allowed_dependencies):
        for dep in base:
            if not (set(self.__table[dep]) - allowed_dependencies):
                yield dep

    def __verify_no_circular_dependencies(self):
        circular = []

        for name in self.__table.keys():
            stack = list(self.__table[name])

            while stack:
                top = stack.pop(0)
                if top == name:
                    circular.append(name)
                    break

                stack.extend(self.__table[top])

        if circular:
            msg = 'The following plugins have circular dependencies: {}'.format(', '.join(circular))
            raise CircularDependencyError(msg)

    def __verify_no_unknown_dependencies(self):
        unknown = []

        for name, deps in self.__table.items():
            if any(dep not in self.__table for dep in deps):
                unknown.append(name)

        if unknown:
            msg = 'The following plugins have unknown dependencies: {}'.format(', '.join(unknown))
            raise UnknownDependencyError(msg)
