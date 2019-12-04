# test.py
import numpy as np


def array_sum(array):
    """funciton for getting sum of array component.

    Parameters
    ----------
    array : ``numpy-array like``
        a target array who is iterable number container.

    Returns
    -------
    ``int`` or ``float``
        summation value of given array.

    """
    return array.sum()

if __name__ == '__main__':
    a = np.array([0,1,2,3])
    print(array_sum(a))
