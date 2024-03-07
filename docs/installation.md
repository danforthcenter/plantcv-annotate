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

### Installing PlantCV for contributors <a name="contributors"></a>
Before getting started, please read our [contributor guidelines](CONTRIBUTING.md) and [code of conduct](CODE_OF_CONDUCT.md).

You can follow the [PlantCV Installation for Contributor Guide](https://plantcv.readthedocs.io/en/latest/installation/#contributors) and then continue with the instructions below to add PlantCV-Annotate to 
your development environment.

```bash
# Activate the plantcv environment (you will have to do this each time you start a new session)
conda activate plantcv
# Install plantcv-annotate in editable mode so that it updates as you work on new features/updates
pip install plantcv-annotate
pip install -e .
```
