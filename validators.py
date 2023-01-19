import typing as t

class BaseDescriptor:
    __set_code__: str = "\tsetattr(inststance, self.name, value)"

    def __init__(self):
        self.name = ""

    def __set_name__(self, owner: object, name: str):
        self.name = f"{type(self).__name__}_{name}"

    def __get__(self, instance: object, meta: t.Optional[type] = None) -> object:
        if instance is None:
            return self
        return getattr(instance, self.name)


class ValidatorMeta(type):
    def __new__(mcs: type, name: str, bases: tuple, clsdict: dict) -> type:
        text = '\n'.join([base.__set_code__
                          for base in reversed(bases)
                          if issubclass(base, BaseDescriptor)])
        return super().__new__(mcs, name, bases, clsdict)


class Fake(metaclass=ValidatorMeta):
    name: str = BaseDescriptor()

