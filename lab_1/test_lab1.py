import numpy as np

from lab1 import my_func


def test_my_func_regular():
    assert np.isclose(my_func(np.float64(1.0)), np.log(2.0))


def test_my_func_zero():
    assert np.isclose(my_func(np.float64(1e-310)), 1.0)
