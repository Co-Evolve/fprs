from __future__ import annotations

import abc
from typing import Iterable, List, Optional, TypeVar

import numpy as np

from fprs import fprs_random_state

T = TypeVar("T")


class Parameter(metaclass=abc.ABCMeta):
    """
    Abstract base class for parameters.
    """

    def __init__(self, value: T) -> None:
        self._value = value

    @property
    @abc.abstractmethod
    def value(self) -> T:
        raise NotImplementedError

    def __eq__(self, other: Parameter) -> bool:
        eq = self.value == other.value
        if isinstance(eq, Iterable):
            eq = all(eq)
        return eq

    @value.setter
    def value(self, value) -> None:
        self._value = value

    def set_random_value(self) -> None:
        raise NotImplementedError


class FixedParameter(Parameter):
    """
    Parameter that never changes its value.
    """

    def __init__(self, value: T) -> None:
        super().__init__(value)

    @property
    def value(self) -> T:
        return self._value

    def __eq__(self, other: Parameter) -> bool:
        eq = self.value == other.value
        if isinstance(eq, Iterable):
            eq = all(eq)
        return eq

    @value.setter
    def value(self, value) -> None:
        raise TypeError("Cannot change the value of a FixedParameter.")


class SynchronizedParameter(FixedParameter):
    """
    Parameter that maintains the value of another parameter.
    """

    def __init__(self, linked_parameter: Parameter) -> None:
        super().__init__(linked_parameter.value)
        self._linked_parameter = linked_parameter

    @property
    def value(self) -> T:
        return self._linked_parameter.value

    def __eq__(self, other: Parameter) -> bool:
        eq = self.value == other.value
        if isinstance(eq, Iterable):
            eq = all(eq)
        return eq

    @value.setter
    def value(self, value) -> None:
        raise TypeError("Cannot set the value of a SynchronizedParameter directly.")


class ContinuousParameter(Parameter):
    """Parameter with a constrained, continuous value. If an initial value is not given, a random value within the
    boundaries will be generated."""

    def __init__(
        self, low: float = -1.0, high: float = 1.0, value: Optional[float] = None
    ) -> None:
        super(ContinuousParameter, self).__init__(value=value)
        self.low = low
        self.high = high

    @property
    def value(self) -> float:
        if self._value is None:
            self.set_random_value()

        self._value = np.clip(self._value, self.low, self.high)
        return self._value

    @value.setter
    def value(self, value) -> None:
        self._value = value

    def set_random_value(self) -> None:
        self._value = fprs_random_state.uniform(low=self.low, high=self.high)


class DiscreteParameter(Parameter):
    """Parameter representing a discrete value from a given list of options."""

    def __init__(self, options: List[T], value: Optional[T] = None) -> None:
        super(DiscreteParameter, self).__init__(value)
        self.options = options

    @property
    def value(self) -> T:
        if self._value is None:
            self.set_random_value()
        return self._value

    @value.setter
    def value(self, value: T) -> None:
        assert (
            value in self.options
        ), f"[DiscreteParameter] Given value '{value}' is not in options '{self.options}'"
        self._value = value

    def set_random_value(self) -> None:
        self._value = fprs_random_state.choice(a=self.options)
