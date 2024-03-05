## Installation

### Table of contents
1. [Supported platforms and dependencies](#dependencies)
2. [Install via a package manager](#install)
    - [PyPI](#pypi)
3. [Installing PlantCV for contributors](#contributors)

### Supported platforms and dependencies <a name="dependencies"></a>
- Linux 64-bit, x86 processors
- macOS x86 (Intel) and M (ARM) processors
- Windows 64-bit, x86 processors

PlantCV requires Python and these [Python packages](https://github.com/danforthcenter/plantcv/blob/main/requirements.txt).
Additionally, we recommend installing [JupyterLab](https://jupyter.org/).

#### PyPI <a name="pypi"></a>

```bash
pip install plantcv

```

Or with optional (but recommended) dependencies:

```bash
pip install plantcv jupyterlab ipympl

```

### Installing PlantCV for contributors <a name="contributors"></a>
Before getting started, please read our [contributor guidelines](CONTRIBUTING.md) and [code of conduct](CODE_OF_CONDUCT.md).

You can build PlantCV from the source code if you are a developer or want the absolute latest version available.
As noted above, we recommend installing PlantCV in a virtual environment. We will outline how to do this using `conda`.
You will also need a [GitHub](https://github.com) account. You will need to
[clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) the PlantCV
repository from GitHub before getting started.

To set up your environment, follow these steps in your command-line terminal:

```bash
# Enter the PlantCV directory
cd plantcv

# Create a conda environment named "plantcv" (or whatever you like) and automatically install the developer dependencies
conda env create -n plantcv -f environment.yml

# Activate the plantcv environment (you will have to do this each time you start a new session)
conda activate plantcv

# Install PlantCV in editable mode so that it updates as you work on new features/updates
pip install -e .

pip install plantcv-annotate
pip install -e .
```
