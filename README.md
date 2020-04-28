# mvgem

mvgem is a tiny CLI application to convert between Genome-scale Metabolic formats.

## Installation process
1. Clone this repository:
```shell
git clone https://github.com/carrascommj/mvgem.git
cd mvgem
```
2. Install the requirements:
```shell
pip install -r requirements.txt
```

3. Put the script under your path. For instance:
```shell
mv mvgem.py ~/.local/bin/mvgem
```
Personally, I prefer to remove the extension.

## Dependencies
All of these packages are specified in the requirements file with pinned versions:
* [click](https://click.palletsprojects.com/en/7.x/): CLI package.
* [cobra](https://opencobra.github.io/cobrapy): IO operations.
* [scipy](https://www.scipy.org): required to handle matlab format.

## Run the application:

    Usage: mvgem.py [OPTIONS] INPUT_MODEL OUTPUT_MODEL

    Convert GEM format INPUT_MODEL to OUTPUT_MODEL.

    The format will be infered based on the extension of OUTPUT_MODEL.
    Supported formats: .sbml, .xml, .json, .mat.

    Options:
      --help  Show this message and exit.
