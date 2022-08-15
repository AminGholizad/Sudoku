from abc import ABC, abstractmethod

import numpy as np
from numpy.typing import NDArray


class Rule(ABC):

    @abstractmethod
    def valid_numbers(self, board: NDArray[np.int_], row: int, col: int) -> NDArray[np.int_]:
        pass

    @abstractmethod
    def is_valid(self, board: NDArray[np.int_]) -> bool:
        pass

    @abstractmethod
    def is_solved(self, board: NDArray[np.int_]) -> bool:
        pass
