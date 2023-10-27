#!/usr/bin/env python3

from pathlib import Path
import shutil
import importlib
import subprocess

import gnuradio

# Get GNU Radio install path
gr_path = Path(gnuradio.path).parent

# Create directory for stubs and clear out old ones
mod_path = Path(__file__).parent
out_path = mod_path / ".output"
stubs_path = out_path / "stubs"
shutil.rmtree(stubs_path, ignore_errors=True)
stubs_path.mkdir(parents=True, exist_ok=True)

# Create a file containing GNU Radio's install path
with open(out_path / "gr_path.txt", "w") as f:
    f.write(str(gr_path.parent))

# Get submodule names
submods = []
for child in gr_path.iterdir():
    if child.is_dir():
        # We only need these stubs for pybind modules, so look for *_python
        submod_name = "gnuradio." + child.name
        pybind_name = str(child.name) + "_python"
        mod_import = importlib.import_module(submod_name)
        if pybind_name in mod_import.__dir__():
            submods += [submod_name]


# Function for invoking stub generation on a module
def stubgen_mod(mod):
    subprocess.run(
        ["pybind11-stubgen", "-o", str(stubs_path), mod, "--ignore-all-errors"]
    )


# Generate stubs
for submod_name in submods:
    print(submod_name)
    stubgen_mod(submod_name)

# Do the same for PMT
stubgen_mod("pmt")

# Clean up the generated stubs
subprocess.run(
    ["black", stubs_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
)
subprocess.run(
    ["isort", "--profile=black", stubs_path],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
