#!/usr/bin/env python
"""Script to convert between GEM models."""
import pickle

import click
from cobra.io import (load_json_model, load_matlab_model, read_sbml_model,
                      save_json_model, save_matlab_model, write_sbml_model)


@click.command()
@click.argument(
    "input-model", type=click.Path(exists=True, dir_okay=False),
)
@click.argument(
    "output-model", type=click.Path(exists=False),
)
def mvgem(input_model, output_model):
    """Convert GEM format INPUT_MODEL to OUTPUT_MODEL.

    The format will be infered based on the extension of OUTPUT_MODEL.
    Supported formats: .sbml, .xml, .json, .mat
    """
    model = load_model(input_model)
    out_format = get_destination_format(output_model)
    if out_format == "SBML":
        write_sbml_model(model, output_model)
    elif out_format == "MAT":
        save_matlab_model(model, output_model)
    elif out_format == "JSON":
        save_json_model(model, output_model)
    else:
        click.BadParameter(
            "Output format %s could not be recognised" % out_format
        ).show()


def get_destination_format(filename):
    """Parse the output `filename` to get the format."""
    out_format = filename.split(".")[-2:]
    out_format = (
        out_format[0].upper()
        if out_format[1].upper() == "GZ"
        else out_format[1].upper()
    )
    if out_format == "XML":
        out_format = "SBML"
    return out_format


def load_model(path_or_handle):
    """Read a metabolic model.

    Adapted from cameo.

    Parameters
    ----------
    path_or_handle : path
        file path of a model file

    """
    if isinstance(path_or_handle, str):
        # Open the given file
        path = path_or_handle
        handle = open(path_or_handle, "rb")
    elif hasattr(path_or_handle, "read"):
        # Argument is already an open file
        path = path_or_handle.name
        handle = path_or_handle
    else:
        click.ClickException(
            f"Provided argument %s has to be either a string or a file handle"
            % path_or_handle
        ).show()
    model = _load_model_from_file(path, handle)  # Parse model from the file

    return model


def _load_model_from_file(path, handle):
    """Try to parse a model from a file handle using different encodings.

    Adapted from cameo.
    """
    try:
        model = pickle.load(handle)
    except (TypeError, pickle.UnpicklingError):
        try:
            model = load_json_model(path)
        except ValueError:
            try:
                model = load_matlab_model(path)
            except ValueError:
                try:
                    model = read_sbml_model(path)
                except AttributeError:
                    click.ClickException(
                        "cobrapy doesn't raise a proper exception"
                        " if a file does not contain an SBML model"
                    ).show()
                except Exception as e:
                    click.ClickException(e).show()
    return model


if __name__ == "__main__":
    mvgem()
