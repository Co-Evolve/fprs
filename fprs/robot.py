from __future__ import annotations

import abc
from abc import ABC
from typing import TypeVar

import numpy as np

from fprs.specification import ControllerSpecification, MorphologySpecification, RobotSpecification

Observations = TypeVar("Observations")
Actions = TypeVar("Actions")


class Robot(ABC):
    """Abstract base class for a robot, which expresses the combination of a Morphology and a Controller."""

    def __init__(
            self,
            specification: RobotSpecification
            ) -> None:
        self._specification = specification
        self._morphology = None
        self._controller = None

    @property
    def morphology(
            self
            ) -> Morphology:
        if self._morphology is None:
            self._morphology = self._build_morphology()
        return self._morphology

    @property
    def controller(
            self
            ) -> Controller:
        if self._controller is None:
            self._controller = self._build_controller()
        return self._controller

    @abc.abstractmethod
    def _build_morphology(
            self
            ) -> Morphology:
        raise NotImplementedError

    @abc.abstractmethod
    def _build_controller(
            self
            ) -> Controller:
        raise NotImplementedError

    @property
    def robot_specification(
            self
            ) -> RobotSpecification:
        return self._specification

    def __call__(
            self,
            observations: Observations
            ) -> Actions:
        return self.controller(observations)


class Morphology(ABC):
    """Abstract base class for a robot's Morphology."""

    def __init__(
            self,
            specification: MorphologySpecification
            ) -> None:
        self._specification = specification

    @property
    def morphology_specification(
            self
            ) -> Morphology:
        return self._specification


class Controller(ABC):
    """Abstract base class for a robot's Controller."""

    def __init__(
            self,
            specification: ControllerSpecification
            ) -> None:
        self._specification = specification

    @property
    def controller_specification(
            self
            ) -> ControllerSpecification:
        return self._specification

    @abc.abstractmethod
    def __call__(
            self,
            observations: np.ndarray
            ) -> np.ndarray:
        """
        Returns actions based on given observations.

        :param observations
        :return: actions
        """
        raise NotImplementedError
