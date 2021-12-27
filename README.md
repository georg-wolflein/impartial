# impartial

A lightweight extension of [functools.partial](https://docs.python.org/3/library/functools.html#functools.partial) that allows modifying positional and keyword arguments in a functional style.
The main idea is that any `impartial` function gets a method `with_<keyword>(value)` for every keyword argument which returns a new `impartial` function with that keyword being modified.

```python
>>> import impartial
>>> @impartial
... def power(x, exponent):
...     return x ** exponent
...
>>> square = power.with_exponent(2) # basically functools.partial(square, exponent=2)
>>> square
impartial(<function power at 0x10d54e790>, exponent=2)
>>> square(3)
9
```

Features:

- the `with_<keyword>(value)` methods can be arbitrarily **chained**
- `impartial` functions are **immutable**: any "modification" of arguments returns a new `impartial` function
- very **lightweight** (~50 LOC)
- fully **compatible** with [functools.partial](https://docs.python.org/3/library/functools.html#functools.partial) (`impartial` is a subclass of `functools.partial`)
- can be used as a **decorator**
