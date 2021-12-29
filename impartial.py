# impartial.py
#
#     https://github.com/georg-wolflein/impartial
#
# Author: Georg Wölflein
#         https://georg.woelflein.eu
#
# Copyright (c) 2021.
#
# Permission is granted to use, copy, and modify this code in any
# manner as long as this copyright message and disclaimer remain in
# the source code.  There is no warranty.

import typing
import inspect
import sys
from functools import partial, partialmethod


def _get_argument_types(func: typing.Callable) -> dict:
    if hasattr(func, "argument_types"):
        return func.argument_types
    signature = inspect.signature(func)
    fargs = [arg.name
             for arg in signature.parameters.values()
             if arg.kind in {inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.KEYWORD_ONLY}]
    type_hints = typing.get_type_hints(func)
    type_hints = {k: type_hints.get(k, None) for k in fargs}
    return type_hints


class impartial(partial):
    """New function with partial application of the given arguments and keywords.

    Every keyword argument can be set using the dynamically generated `with_<keyword>(value)` methods, returning a new impartial function.
    Positional arguments can be appended using the `configure(*args, **keywords)` method.
    Fully compatible with functools.partial.
    """

    def __new__(cls, func: typing.Union[typing.Callable, partial, "impartial"],
                *args,
                _first_arg_is_self: bool = False,
                **keywords) -> "impartial":
        argument_types = None
        if hasattr(func, "func"):
            args = func.args + args
            keywords = {**func.keywords, **keywords}
        while hasattr(func, "func"):
            if argument_types is None and hasattr(func, "argument_types"):
                argument_types = func.argument_types
            func = func.func
        if argument_types is None:
            argument_types = _get_argument_types(func)
        self = super().__new__(cls, func, *args, **keywords)
        self.argument_types = argument_types
        self._first_arg_is_self = _first_arg_is_self

        for arg, arg_type in self.argument_types.items():
            if arg == "self" and self._first_arg_is_self:
                continue
            func_name = f"with_{arg}"
            setattr(self, func_name,
                    self._make_setter(arg, func_name, arg_type))
        return self

    def _make_setter(self, arg_name: str, func_name: str, type_hint: type = None) -> typing.Callable:
        def setter(value) -> "impartial":
            return self.__class__(self, **{arg_name: value})
        setter.__name__ = func_name
        setter.__doc__ = f"Set {arg_name}"
        if type_hint is not None:
            setter.__annotations__["value"] = type_hint
        return setter

    def configure(self, *args, **keywords) -> "impartial":
        """Set arguments and keyword arguments.

        Returns:
            impartial: function with the given arguments and keywords
        """
        return self.__class__(self, *args, **keywords)

    def __call__(self, /, *args, **keywords):
        return super().__call__(*args, **keywords)


class impartialmethod(partialmethod):
    """Equivalent of functools.partialmethod."""

    def __get__(self, obj, cls=None):
        # Copied from functools.partialmethod, but with a call to impartial() instead of partial()
        get = getattr(self.func, "__get__", None)
        result = None
        if get is not None:
            new_func = get(obj, cls)
            if new_func is not self.func:
                result = impartial(new_func, *self.args, **self.keywords)
                try:
                    result.__self__ = new_func.__self__
                except AttributeError:
                    pass
        if result is None:
            result = self._make_unbound_method().__get__(obj, cls)
        return result


impartial.method = impartialmethod
sys.modules[__name__] = impartial
