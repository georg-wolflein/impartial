# impartial

[![build](https://github.com/georg-wolflein/impartial/workflows/build/badge.svg)](https://github.com/georg-wolflein/impartial/actions?query=workflow%3Abuild)
[![PyPI](https://img.shields.io/pypi/v/impartial)](https://pypi.org/project/impartial)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/impartial)](https://pypi.org/project/impartial)
[![Licence](https://img.shields.io/github/license/georg-wolflein/impartial)](https://github.com/georg-wolflein/impartial/blob/master/LICENSE)

_impartial_ is a lightweight extension of [functools.partial](https://docs.python.org/3/library/functools.html#functools.partial) that allows modifying positional and keyword arguments in a functional style.

The main idea is that any function wrapped with `impartial` gets a method `with_<keyword>(value)` for every keyword argument of that function.
Each `with_<keyword>(value)` method returns a new `impartial` function with that keyword being modified.

```python
>>> import impartial
>>> @impartial
... def power(x, exponent):
...     return x ** exponent
...
>>> power
impartial(<function power at 0x10d54e790>)
>>> square = power.with_exponent(2) # behaves like functools.partial(square, exponent=2)
>>> square
impartial(<function power at 0x10d54e790>, exponent=2)
>>> square(3)
9
```

Features:

- the `with_<keyword>(value)` methods can be arbitrarily **chained**
- `impartial` functions are **immutable**: any "modification" of arguments returns a new `impartial` function
- very **lightweight** (~50 LOC and no dependencies)
- fully **compatible** with [functools.partial](https://docs.python.org/3/library/functools.html#functools.partial) (`impartial` is a subclass of `functools.partial`)
- can be used as a **decorator**

To install this package, run:

```
pip install impartial
```
