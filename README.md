# mestDS

**mestDS** (https://github.com/martin-og-ingar/mestDS/tree/ingar/pipeline-model-assesment) is a Python library for **time series simulation** and **model evaluation**, designed to work seamlessly with **CHAP-core models**.

This documentation explains how to use the domain-specific language (DSL) developed for the **mestDS framework**. The DSL allows users to configure simulators and evaluators in a flexible, reusable, and effective way.

## Table of Contents

- [Installation](#installation)
- [Overview](#dsl-overview)
- [Defining Simulators](#defining-simulators)
  - [Simulator Structure](#simulator-structure)
  - [Public Functions and Lists](#public-functions-and-lists)
  - [Inheritance](#inheritance)
- [Defining Evaluators](#defining-evaluators)
- [Using mestDS](#using-mestds)

## Installation

This project depends on several Python packages that may require careful version management. The instructions below ensure a smooth setup:

#### 1. Create a virtual environment

Make sure to use Python 3.11 and to have version 3.11.3 installed on your system.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade "pip==24.0"
```

Furthermore, pyenv (https://github.com/pyenv/pyenv) is required when running a model through the chap-core repository. Make sure it is installed as well:

```bash
pyenv --version
```

#### 2. Install mestDS and other packages

Install only mestDS (not it's required packages):

```bash
pip install mestDS --no-deps
```

Install chap-core:

```bash
pip install chap-core
```

Lastly, install fpdf:

```bash
pip install fpdf2
```

#### 3. Test setup

Run **script.py** to check if the setup works:

```bash
python3.11 script.py
```

## DSL Overview

The DSL is composed of two main components:

1. **Simulator configurations** – define synthetic datasets, including variable generation logic.
2. **Evaluator configurations** – define evaluation logic for models, specifying metrics, prediction lengths, and other parameters.

These configurations populate instances of the `Simulator` and `Evaluator` classes within the framework.

The DSL is defined in a YAML file, which is passed to a mestDS object in a python script.

## Defining Simulators

### Simulator Structure

A simulator instance is defined as a YAML mapping under the top-level key `simulators`. Each simulator defines its variables (`x` for inputs, `y` for outputs) either via inline Python functions or references to **public functions**.

Example:

```yaml
simulators:
  - id: 1
    name: train with no random spike
    description: Is the model detecting the seasonality or time lag?
    time_delta: M
    length: 100
    x:
      - name: rainfall
        function_ref: get_rainfall_spike
        params:
          random_spikes: [93]
      - name: population
        function: |
          def get_flat_value():
              return np.random.normal(1000, 5)
      - name: mean_temperature
        function: |
          def get_flat_value():
              return np.random.normal(27, 3)
    y:
      - name: disease_cases
        function_ref: get_disease_cases_with_lag
        params:
          lag: 3
```

### Public Functions and Lists

To improve code reuse, the DSL supports public functions and lists that can be referenced by multiple simulators.

Example:

```yaml
public:
  functions:
    get_flat_value: |
      def get_flat_value(mean, randomness):
        return np.random.normal(mean, randomness)
    get_rainfall_spike: |
      def get_rainfall(i, seasonal_spikes, random_spikes):
        if i in seasonal_spikes or i in random_spikes:
          return 50
        else:
          return 10
    get_disease_cases_with_lag: |
      def get_disease_cases_with_lag(rainfall, lag):
        if len(rainfall) < lag:
          return int(rainfall[-1])
        return int(rainfall[-lag])
  lists:
    seasonal_spikes: [5, 17, 29, 41, 53, 65, 77, 89]
```

- **function_ref** references a function defined in public.functions.

- **params** supplies the arguments for the function.

- **lists** provide shared data (e.g., seasonal_spikes).

### Inheritance

The DSL supports inheritance of simulator configurations to avoid duplication. Use the inherit key to base a new simulator on an existing one and override only specific parts.

Example:

```yaml
simulators:

- id: 1
  name: train with no random spike
  ...
- id: 2
  inherit: 1
  name: train with one random spike
  description: Model trained with one random spike added
  x:
  - name: rainfall
    params:
    random_spikes: [56, 93]
```

This creates a new simulator (ID 2) based on simulator 1, modifying only the rainfall spikes.

## Defining Evaluators

Evaluator instances configure model evaluation. Each evaluator specifies:

- The model (local path or Git repository)

- Prediction length

- Stride

- Number of test sets

- Metrics to compute

- Optional simulation overrides (time_delta, sim_length)

Example:

```yaml
evaluators:
  - model: https://github.com/dhis2-chap/ewars_template.git
    prediction_length: 3
    stride: 2
    n_test_sets: 6
    metrics: [mse, pocid, theils_u]
    plot_length: 100
  - model: models/weekly_ar_model/
    sim_length: 300
    time_delta: W
    prediction_length: 12
    stride: 12
    n_test_sets: 3
    metrics: [mse, pocid, theils_u]
    plot_length: 100
```

The DSL allows overriding simulator parameters for specific evaluator instances, providing flexibility for different model requirements.

## Using mestDS

The mestDS component serves as the user interface to interact with the framework. It:

- Parses the DSL

- Manages Simulator and Evaluator instances

- Provides utility methods for simulation, evaluation, data export, and visualization

Key methods:

- simulate() – runs all simulators

- evaluate() – evaluates models across simulators

- to_csvs() – exports simulated data to CSV

- plot_data() – visualizes simulation results

Example usage:

```python
from mestDS import mestDS

# Load DSL configuration
_mestds = mestDS("my_config.yaml")

# Run simulations
sims = _mestds.simulate()

# Evaluate models
_mestds.evaluate(sims)
```

OR

```python
from mestDS import mestDS

# Load DSL configuration
_mestds = mestDS("evaluator_configs.yaml")

# Evaluate models on existing data
_mestds.evaluate("brazil-dengue.csv")
```
