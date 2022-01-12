from functools import partial

from impartial import impartial


def f(x: int, y: int, z: int = 0) -> int:
    return x + 2*y + z


def test_simple_call_args():
    assert impartial(f, 1)(2) == f(1, 2)


def test_simple_call_kwargs():
    assert impartial(f, y=2)(x=1) == f(1, 2)


def test_simple_call_empty():
    assert impartial(f, 1, y=2)() == f(1, 2)


def test_decorator():
    @impartial
    def f(x, y):
        return x + 2*y
    assert f.with_y(2)(1) == 5


def test_func():
    assert impartial(f, 1).func is f


def test_with_kwargs():
    assert impartial(f, 1).with_z(3)(2) == f(1, 2, 3)


def test_multiple_with_kwargs():
    assert impartial(f, 1).with_z(3).with_y(2)() == f(1, 2, 3)


def test_with_kwargs_override():
    assert impartial(f, 1, 2).with_z(3).with_z(4)() == f(1, 2, 4)


def test_nested_impartial():
    imp = impartial(f, x=1, y=2)
    imp = impartial(imp, x=2)
    imp = impartial(imp, x=3)
    assert imp() == f(3, 2)
    assert not isinstance(imp.func, impartial)
    assert imp.func is f


def test_nested_partial():
    imp = partial(f, x=1, y=2)
    imp = partial(imp, x=2)
    imp = impartial(imp, x=3)
    assert imp() == f(3, 2)
    assert not isinstance(imp.func, partial)
    assert imp.func is f


def test_configure():
    assert impartial(f, 1, z=2).configure(2, z=3)() == f(1, 2, 3)
