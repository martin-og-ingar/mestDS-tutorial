# mestDS - Introduction to mestDS

**mestDS** is a Python library for **time series simulation** and **model evaluation**, designed to work seamlessly with **CHAP-core models**.

This tutorial gives an introduction to how the **mestDS** framework can be utilized. This tutorial assumes that the prerequsites for running a model through `chap-core`, and `mestD` are installed, as described in the [installation guide](README.md).

## 1. Define a simplisitc Simulator

Let's start off by defining a simplistic simulation in the domain-specific language (DSL).

Start with creating a `yaml`-file, which is the langauge the DSL uses, and is where the `Simulators` and `Evaluators` are defined. Some knowledge about `YAML` is benefitial, but not required, as it is pretty simplistic.

All `Simulator` instances are defined inside the top-level `simulators` keyword. Inside the `simulators` keyword, a `Simulator` instance is defined as a list item of the `simualtors`keyword:

```yaml
simulators:
  - <-- Each tick defines one Simulator instance.
```

Let's continue by populating some of the variables of the `Simulator` instance, more precisely `id`, `name`, `description`, `time_delta`, `length`:

```yaml
simulators:
  - id: 1
    name: 1st Simplistic Simulator
    description: This is very simplistic simulation
    time_delta: M
    length: 100
```

Considerations from the previous code snippet:

- Give the `Simulator` instance an id, so we can reference it later in the tutorial.
- Define a fitting name and description. This is especially benefitial for keeping track when the number of instances grow.
- In this example, we are simulatiing time series with a monthly time step, and a total of 100 months.

Now we are just missing the `x` and `y` features. These are defined as list items inside the `x`and `y` keywords, just like the `Simulator` instances inside the `simulator` keyword:

```yaml
simulators:
  - id: 1
    name: 1st Simplistic Simulator
    description: This is very simplistic simulation
    time_delta: M
    length: 100
    x:
      - name: rainfall
        function: |
          def get_rainfall(): # rainfall
            return np.random.randint(0,30)
      - name: mean_temperature
        function: |
          def get_temp(): # mean temperature
            return np.random.randint(20,30)
    y:
      - name: disease_cases
        function: |
          def get_dc(rainfall, mean_temperature): # disease cases
            return int(rainfall[-1]*0.5 + mean_temperature[-1]*0.5)
```

Considerations from the previous code snippet:

- In the example, features inside `x` and `y` are assigned their own name and function.
- It is important to add a **|** (pipe) after `function:`. The indentation is alos important!
- The `disease_cases` function has `rainfall` and `mean_temperature` in the argument list, and can therefore access their list of values. In this case, the function is using their last values to calculate the number of disease cases.
- For `chap-core` models, disease cases are expected to be an integer, so cast the value before returning.

Thats it! The previous `YAML` snippet is all that is required to define a simplistic `Simulator` instance.

Let's try to initialize the `mestDS` framework with the DSL:

```python
from mestDS import mestDS

_mestds = mestDS("my_config.yaml")
_mestds.simulate()
_mestds.plot_data()
```

Add a folder path to the `plot_data` function if you want to store the plot persistantly:

```python
from mestDS import mestDS

_mestds = mestDS("my_config.yaml")
_mestds.simulate()
_mestds.plot_data("plots")
```

## 2. Define an Evaluator

Now lets add an `Evaluator` instance to the DSL, to complete the full time series simulation model evaluation pipeline. `Evaluator` instances are defined as list items inside the top-level keyword `evaluators`:

```yaml
evaluators:
  - model: https://github.com/dhis2-chap/ewars_template.git
    prediction_length: 3
    stride: 2
    n_test_sets: 6
    metrics: [mse, pocid, theils_u]
    plot_length: 100
```

Consideration from the previous code snippet:

- The model we want to evaluate on the simplistic simulation defined in the previous section is defined in the `model` keyword. In this example, we have passed a git repo, but it could also be the path a local model.
- The prediction length defines how far each prediction is. This is often specific for `chap-core` models, so this requires own investigation of your chosen model.
- `n_test_sets` and `stride` defines how many predictions are made, and how far each prediction jumps from the previous prediction. In our example:
  - The first prediction of the model evaluation starts at 12 months (6*2) from the end of the time series. The second prediction start at 10 months (5*2) from the end of the time series, the tirds starts at 8 months (4*2) from the end of the time series, ...., the last prediction starts at 2 months (1*2) from the end of the time series.
- Metrics can vary depending on the time series. In this case, we have chosen MSE, POCID and Theils U.
- When the dataset becomes very large (e.g. 1000 months), setting a defined length of the plot can be useful to see the details of the plot properly.

`chap-core` models requries the features time_period, location and population, along with the features we defined in the previous section, namely rainfall, mean_temperautre and disease_cases. `mestDS` takes care of time_period and location, but population must be added to the DSL. In the following code snippet, all the required features are added to the simplistic `Simulator` instance, along with the `Evaluator` definition:

```yaml
simulators:
  - id: 1
    name: 1st Simplistic Simulator
    description: This is very simplistic simulation
    time_delta: M
    length: 100
    x:
      - name: population
        function: |
          def get_population(): # population
            return np.random.randint(1000, 1010)
      - name: rainfall
        function: |
        def get_rainfall(): # rainfall
          return np.random.randint(0,30)
      - name: mean_temperature
        function: |
        def get_temp(): # mean temperature
          return np.random.randint(20,30)
    y:
      - name: disease_cases
        function: |
        def get_dc(rainfall, mean_temperature): # disease cases
          return int(rainfall[-1]*0.5 + mean_temperature[-1]*0.5)
evaluators:
  - model: https://github.com/dhis2-chap/ewars_template.git
    prediction_length: 3
    stride: 2
    n_test_sets: 6
    metrics: [mse, pocid, theils_u]
    plot_length: 100
```

Now we can update our Python script to simulate and evaluate the model:

```python
from mestDS import mestDS

_mestds = mestDS("my_config.yaml")
_mestds.simulate()
_mestds.evaluate()
```

And after running the script, a model evaluation report should be stored as a pdf with the name: [], and should contain a table of the performance metrics and a plot of the predictions:

![Result from the simplistic model evaluation](simple_eval.png?raw=true)

## 3. Simplify the simplistic Simulator definition

As you might have noticed, the features' functions in the simplistic `Simulator` instance are basically doing the same thing, returning a random value within an interval. Let make the definition of the simplistic `Simulator` even more simplistic, by incorporating public functions!

The following code snippet includes a public function called get_random_value, which is referenced in the feature definitions. Furthermore, the the function has two arguments: the min and max value of the the random value:

```yaml
public:
  functions:
    - get_random_value: |
        get_ranfom_value(min, max)_
          return np.random.randint(min, max)
simulators:
  - id: 1
    name: 1st Simplistic Simulator
    description: This is very simplistic simulation
    time_delta: M
    length: 100
    x:
      - name: population
        function_ref: get_random_value
        params:
          min: 1000
          max: 1010
      - name: rainfall
        function_ref: get_random_value
        params:
          min: 0
          max: 30
      - name: mean_temperature
        function_ref: get_random_value
        params:
          min: 20
          max: 30
```

## 4. Adding another Simulator

A single simulated time series is not sufficient for a thurough model evaluation. Let's add another!

In the second Simulator, we wish to keep most of the same features and variable values from the initial Simulator, but adjust the weights of rainfall and temperature when calculating disease cases. In order to do so, we have also added the disease case function to the list of public functions and parameterized rainfall and mean_temperature's weights:

```yaml
public:
functions:
  - get_random_value: |
    get_ranfom_value(min, max): # return a random value
      return np.random.randint(min, max)
  - get_dc: |
    get_dc(rainfall, rainfall_weight, mean_temperature, temp_weight): #return disease cases
      return int(rainfall[-1] * rainfall_weight + mean_temperature[-1] * temp_weight)
simulators:
  - id: 1
    name: 1st Simplistic Simulator
    description: This is very simplistic simulation
    time_delta: M
    length: 100
    x: ... the same features as before
    y:
      - name: disease_cases
        function_ref: get_dc
        params:
          rainfall_weight: 0.5
          temp_weight: 0.5
  - id: 2
    inherit: 1
    y:
      - name: disease_cases
        params:
          rainfall_weight: 0.7
          temp_weight: 0.3
```

Considerations from the previous code snippet:

- Ignore the wrong formatting of the python function!
- Since the second `Simulator` is just adjusting the weights of rainfall and mean_temperature in the disease case function, we can simply copy the initial `Simulator` instance by passing the `id` to the `inherit` keyword, and override the arguments.

## That's it!

Now you should get the gist of `mestDS`. Moving forward, you can check out the more detailed [documentation of the DSL](documentation.md) and explore all of the posibilities of the framework.

You can also check the [introduction to MIMES](mimes.md)
