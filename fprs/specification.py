from __future__ import annotations

import abc
import pickle
from typing import Iterable, List

from fprs.parameters import Parameter


class Specification(metaclass=abc.ABCMeta):
    """Abstract base class to represent a parameterized robot morphology or controller specification. Specifications
    can be saved as pickle files and loaded from pickle files."""

    def __init__(
            self
            ) -> None:
        pass

    @property
    def parameters(
            self
            ) -> List[Parameter]:
        parameters = []
        for field_name in vars(self):
            field = self.__getattribute__(field_name)
            if isinstance(field, Parameter):
                parameters.append(field)
            elif isinstance(field, Iterable) and not isinstance(field, str):
                for spec in field:
                    if isinstance(spec, Specification):
                        parameters += spec.parameters
            elif isinstance(field, Specification):
                parameters += field.parameters
        return parameters

    def save(
            self,
            path: str
            ) -> None:
        with open(path, 'wb') as handle:
            pickle.dump(self, handle, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load(
            path: str
            ) -> Specification:
        with open(path, 'rb') as handle:
            return pickle.load(handle)


class RobotSpecification(Specification, metaclass=abc.ABCMeta):
    """Abstract base class to represent a parameterized robot specification, which combines a parameterized morphology
    specification and a parameterized controller specification."""

    def __init__(
            self,
            morphology_specification: MorphologySpecification,
            controller_specification: ControllerSpecification
            ) -> None:
        super().__init__()
        self._morphology_specification = morphology_specification
        self._controller_specification = controller_specification

    @property
    def morphology_specification(
            self
            ) -> MorphologySpecification:
        return self._morphology_specification

    @property
    def controller_specification(
            self
            ) -> ControllerSpecification:
        return self._controller_specification


class MorphologySpecification(Specification, metaclass=abc.ABCMeta):
    """Abstract base class to represent a parameterized morphology specification."""

    def __init__(
            self
            ) -> None:
        super().__init__()


class ControllerSpecification(Specification, metaclass=abc.ABCMeta):
    """Abstract base class to represent a parameterized controller specification."""

    def __init__(
            self
            ) -> None:
        super().__init__()
