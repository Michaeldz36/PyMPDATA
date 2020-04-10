"""
Created at 03.2020
"""

import numpy as np
from .indexers import make_flag, indexers, MAX_DIM_NUM
from ..arakawa_c.boundary_condition.constant import Constant


class ScalarField:
    def __init__(self, data: np.ndarray, halo: int, boundary_conditions):
        self.n_dims = data.ndim
        shape_with_halo = [data.shape[i] + 2 * halo for i in range(self.n_dims)]
        self.data = np.zeros(shape_with_halo, dtype=np.float64)
        self.halo = halo
        self.domain = tuple([slice(self.halo, self.data.shape[i] - self.halo) for i in range(self.n_dims)])
        self.get()[:] = data[:]
        self.fill_halos = tuple(
            [(boundary_conditions[i] if i < self.n_dims else Constant(np.nan)).make_scalar(indexers[self.n_dims].at[i], halo)
             for i in range(MAX_DIM_NUM)])
        self.boundary_conditions = boundary_conditions
        self.flag = make_flag(False)

    @staticmethod
    def clone(field):
        return ScalarField(field.get(), field.halo, field.boundary_conditions)

    def get(self) -> np.ndarray:
        results = self.data[self.domain]
        return results

    @property
    def impl(self):
        return (self.flag, self.data), self.fill_halos

    @staticmethod
    def make_null(n_dims):
        null = ScalarField(np.empty([0]*n_dims), halo=0)
        null.flag[0] = True
        return null
