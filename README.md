# Framework for Parameterized Robot Specifications (FPRS)

This Python package introduces a framework for the definition and standardization of parameterized robot
specifications, facilitating their use in optimization contexts. Central to this framework are abstract classes designed
to streamline the process of creating detailed robot specifications. A robot, in this context, is conceptualized as an
entity comprising two primary components: morphology and controller. Each of these components is characterized by its
unique parameterized specification.

These parameterized specifications serve a dual purpose. Firstly, they consolidate all configurable attributes of a
robot, thereby providing a comprehensive overview of its characteristics. Secondly, and more critically, they render
these attributes amenable to optimization.

## Installation

`python -m pip install git+https://github.com/Co-Evolve/fprs`
