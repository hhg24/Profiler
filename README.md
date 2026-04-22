# Introduction 
This is a project template for analytical pipelines based on SQL files or statements running in Python. It uses the SQLAlchemy library to access the database.

The current functionality includes:
    - Create connections to the database through a Connection class, see `/src/connection.py`.
    - Read parametrised SQL files or statements and execute queries or save pandas DataFrames object, see `/src/read.py`.
    - Write tables resulting from SQL queries as Excel files see `/src/write.py`.

This is a work in progress project. Stay tuned for more updates!

# Getting started

## Environment management

You can use conda´s commands below to create and activate the environment. 
Check [conda´s Getting Started](https://docs.conda.io/projects/conda/en/stable/user-guide/getting-started.html) guide for more information.

```
# create and activate conda environment
conda env create -f environment.yml
conda activate environment_name
```

## Running scripts

You can check the example.py as a template for an analytical script creating a TEMP table, querying it and writing the result in a Excel file under `/results/`.

```
# run example script
python example-py
```

## Advanced option: uv 

Alternatively you can use uv as a package and environment manager. uv is a fast Python package and project manager, written in Rust.
For more info check the [uv's Getting Started](https://docs.astral.sh/uv/getting-started/) or [MLOps in Databricks Confluence](https://layagroup.atlassian.net/wiki/spaces/LS/pages/9075687444/MLOps+in+Databricks+-+Course+-+Project#1.-Set-up-of-the-project-infrastructure:)

- Use this command to install uv in Windows. More info on [Installation](https://docs.astral.sh/uv/getting-started/installation/)

```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

-  By using the `uv run` command, a virtual environment gets created automatically based on the uv.lock file existing in the repo. More info on [Running commands](https://docs.astral.sh/uv/guides/projects/#running-commands)

```
uv run example.py
```

- You can also create virtual environments, install packages from a pyproject.toml file,  add new packages and lock the dependencies   

```
# Create a virtual environment with a specific Python version
uv venv -p 3.11 .venv
# Install packages defined in a pyproject.toml file, --all-extras install also optional dependencies
uv pip install -r pyproject.toml --all-extras
# to add packages and update pyproject.toml
uv add package
# to lock dependencies in uv.lock file
uv lock
```

- For compatibility with conda, you can write the dependencies from the pyproject.toml file to a requirements.txt or environment.yml files:

```
# to save a requirements.txt file
uv pip compile pyproject.toml -o requirements.txt
# to create an environment.yml file
uv run src/utils/create_env_file.py
```