# mestDS - Installation

**mestDS** is a Python library for **time series simulation** and **model evaluation**, designed to work seamlessly with **CHAP-core models**.

The following demonstrates how to set up an environment for running `mestDS` and models through `chap-core`(https://github.com/dhis2-chap/chap-core).

After completing the set up below, try following these steps for an deeper understanding of `mestDS` and how it can be utilized:

1. Complete the [introduction to mestDS](tutorial.md).
2. Explore the [documentation of the DSL](documentation.md) to learn more about `mestDS`'s posibilities.
3. Complete the introduction to [Mechanism-Isolated Model Evaluations (MIMES)](mimes.md). This introduces an approach to using simulated time series for model evaluation, an area that remains relatively unexplored in the literature. It highlights both the value of the MIMES approach and the strengths of mestDS, which is particularly well-suited for this approach.

## Installation

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

### 2. Install mestDS

> **Plase note:** A MacOS user experienced problems with running models with `chap-core` through `mestDS` without explicitly using `Python 3.11.3`. This can be solved in multiple ways, but because you have already installed `pyenv` by following this tutorial, you can simply create a pyenv shell with the correct version: `pyenv shell 3.11.3`.

> **Furthermore:** The author of this tutorial recommend using a clean virtual environment of some sort (e.g. venv, conda, etc.) Those often allow you to create a virtual environment with a specific `Python` version.

Now it is time to install `mestDS` with `pip`:

```bash
pip install mestDS==0.0.4
```

### 4. Test setup

You can verify that the setup is working by cloning this repository and running the simplistic script:

```bash
git clone https://github.com/martin-og-ingar/mestDS-tutorial.git
python script.py
```
