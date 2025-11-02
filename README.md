# mestDS - Installation

**mestDS** is a Python library for **time series simulation** and **model evaluation**, designed to work seamlessly with **CHAP-core models**.

The following demonstrates how to set up an environment for running `mestDS` and models through `chap-core`(https://github.com/dhis2-chap/chap-core).

After completing the set up below, try following these steps for an deeper understanding of `mestDS` and how it can be utilized:

1. Complete the [introduction to mestDS](tutorial.md).
2. Explore the [documentation of the DSL](documentation.md) to learn more about `mestDS`'s posibilities.
3. Complete the introduction to [Mechanism-Isolated Model Evaluations (MIMES)](mimes.md). This introduces an approach to using simulated time series for model evaluation, an area that remains relatively unexplored in the literature. It highlights both the value of the MIMES approach and the strengths of mestDS, which is particularly well-suited for this approach.

## Installation

This project depends on several Python packages that may require careful version management. The instructions below ensure a smooth setup:

### 1. Installing pyenv and Python 3.11.3

A prerequisite for running models through chap-core, is having Python 3.11.3 installed on your system.
This guide explains how to install pyenv (a simple Python version manager) and use it to install Python 3.11.3 on your system.

#### What is pyenv?

pyenv lets you easily install and manage multiple versions of Python on the same computer. It’s great for development environments where different projects need different Python versions.

#### 1.2 Install prerequisites

Before installing pyenv, make sure your system has the build dependencies required for compiling Python.

Ubuntu / Debian:

```bash
sudo apt update
sudo apt install -y make build-essential libssl-dev zlib1g-dev \
 libbz2-dev libreadline-dev libsqlite3-dev curl llvm \
 libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev \
 libffi-dev liblzma-dev git
```

macOS (using Homebrew):

```bash
brew update
brew install openssl readline sqlite3 xz zlib git
```

#### 1.3 Install pyenv

Clone the pyenv repository:

```bash
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
```

Add pyenv to your shell by appending the following to your ~/.bashrc (or ~/.zshrc if you use Zsh):

```bash
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
if command -v pyenv >/dev/null 2>&1; then
  eval "$(pyenv init -)"
fi
```

Apply the changes:

```bash
source ~/.bashrc
```

Verify pyenv installation:

```bash
pyenv --version
```

#### 1.4 Install Python 3.11.3

Use pyenv to install the specific Python version:

```bash
pyenv install 3.11.3
```

### 2. Set up Python virtual environment

This guide recommends using a Python virtual environment for installing packages:

```bash
python -m venv .venv
source .venv/bin/activate
```

#### 2.2 Install the required packages:

Due to version conflicts, the packages must be installed with careful considerations.

Install only mestDS (not it's required packages):

```bash
pip install mestDS --no-deps
```

Install chap-core:

```bash
pip install chap-core
```

This will likely result in an error about version conflicts, but this can be ignored.

Lastly, install fpdf:

```bash
pip install fpdf2
```

### 4. Test setup

You can verify that the setup is working by cloning this repository and running the simplistic script:

```bash
git clone https://github.com/martin-og-ingar/mestDS-tutorial.git
python script.py
```

Once everything is up and running, you can check out the [introduction to mestDS](tutorial.md), for a simple and progressive introduction to how the framework can be used. A [documentation for the **domain-specific language (DSL)**](documentation.md) is also provided, which describes how the DSL is structured and how **Simulators** and **Evaluators** are defined. Lastly, a
