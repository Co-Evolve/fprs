from __future__ import annotations

import abc
from typing import Callable, List

from fprs.parameters import FixedParameter, Parameter
from fprs.specification import (
    ControllerSpecification,
    MorphologySpecification,
    RobotSpecification,
    Specification,
)


class SpecificationParameterizer(metaclass=abc.ABCMeta):
    """Abstract base class for specification parameterizers, i.e. classes that change specific FixedParameters to
    non-FixedParameters."""

    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def parameterize_specification(self, specification: Specification) -> None:
        raise NotImplementedError

    def get_target_parameters(self, specification: Specification) -> List[Parameter]:
        target_parameters = []
        for parameter in specification.parameters:
            if not isinstance(parameter, FixedParameter):
                target_parameters.append(parameter)
        return target_parameters

    def num_target_parameters(self, specification: Specification) -> int:
        target_parameters = self.get_target_parameters(specification)
        num_parameters = len(target_parameters)
        return num_parameters


class RobotSpecificationParameterizer(
    SpecificationParameterizer, metaclass=abc.ABCMeta
):
    """Abstract base class for robot specification parameterizers, which combines a morphology specification
    parameterizer with a controller specification parameterizer."""

    def __init__(
        self,
        specification_generator: Callable[[], RobotSpecification],
        morphology_parameterizer: MorphologySpecificationParameterizer,
        controller_parameterizer: ControllerSpecificationParameterizer,
    ) -> None:
        super().__init__()
        self._specification_generator = specification_generator
        self._morphology_parameterizer = morphology_parameterizer
        self._controller_parameterizer = controller_parameterizer

    def parameterize_specification(self, specification: RobotSpecification) -> None:
        self._morphology_parameterizer.parameterize_specification(
            specification.morphology_specification
        )
        self._controller_parameterizer.parameterize_specification(
            specification.controller_specification
        )

    def generate_parameterized_specification(self) -> RobotSpecification:
        robot_specification = self._specification_generator()
        self.parameterize_specification(robot_specification)
        return robot_specification

    def get_target_parameters(
        self, specification: RobotSpecification
    ) -> List[Parameter]:
        morphology_parameters = self._morphology_parameterizer.get_target_parameters(
            specification.morphology_specification
        )
        controller_parameters = self._controller_parameterizer.get_target_parameters(
            specification.controller_specification
        )
        return morphology_parameters + controller_parameters

    def get_parameter_labels(self, specification: RobotSpecification) -> List[str]:
        morphology_labels = self._morphology_parameterizer.get_parameter_labels(
            specification.morphology_specification
        )
        controller_labels = self._controller_parameterizer.get_parameter_labels(
            specification.controller_specification
        )
        return morphology_labels + controller_labels


class MorphologySpecificationParameterizer(
    SpecificationParameterizer, metaclass=abc.ABCMeta
):
    """Abstract base class to represent a morphology specification parameterizer."""

    def __init__(self) -> None:
        super().__init__()

    @abc.abstractmethod
    def parameterize_specification(
        self, specification: MorphologySpecification
    ) -> None:
        raise NotImplementedError

    def get_parameter_labels(self, specification: MorphologySpecification) -> List[str]:
        return []


class ControllerSpecificationParameterizer(
    SpecificationParameterizer, metaclass=abc.ABCMeta
):
    """Abstract base class to represent a controller specification parameterizer."""

    def __init__(self) -> None:
        super().__init__()

    @abc.abstractmethod
    def parameterize_specification(
        self, specification: ControllerSpecification
    ) -> None:
        raise NotImplementedError

    def get_parameter_labels(self, specification: ControllerSpecification) -> List[str]:
        return []
