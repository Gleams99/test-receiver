"""
Python script to act as the common entry point for test execution


"""

import os
import sys
from dataclasses import dataclass

import click
import pytest
from rich import print
from rich.console import Console

from config import TESTS_DIR

console = Console()


class TargetEnvironmentNotSpecified(Exception):
    """The target environment was not specified explicitly or by environment variable"""


class UnknownTestExecutionConfig(Exception):
    """The supplied Test Execution Config was not found in the lookup"""


@dataclass
class TestExecutionConfig:
    target_env: str
    pytest_args: str


PREDEFINED_CONFIGS = {
    "All_Tests": TestExecutionConfig(
        target_env="Internal",
        pytest_args="--filter-location config/filter_specs/filter_all.json",
    ),
    "Blue_or_green": TestExecutionConfig(
        target_env="Internal",
        pytest_args="--filter-location config/filter_specs/filter_blue_or_green.json",
    ),
    "Red_and_yellow": TestExecutionConfig(
        target_env="Internal",
        pytest_args="--filter-location config/filter_specs/filter_yellow_and_red.json",
    ),
    "Grey": TestExecutionConfig(
        target_env="Internal",
        pytest_args="--filter-location config/filter_specs/filter_grey.json",
    ),
    "Collect_Tests": TestExecutionConfig(
        target_env="Internal",
        pytest_args="--filter-location config/filter_specs/sample_filter.json --collect-only "
        "--json-report-file=collected_tests.json",
    ),
}


def config_lookup(config):
    """
    Configs should not define the parallelisation arguments.
    Instead a '_X' can be added to the end of the provided config name.
    The pytest args will automatically be updated with "-n auto"

    """
    parallel_args = ""
    if config.endswith("_X"):
        config = config[:-2]
        parallel_args = " -n auto"
    try:
        f = PREDEFINED_CONFIGS[config]
    except KeyError:
        raise UnknownTestExecutionConfig(f"Supplied Test Execution Config [{config}]")
    return f.target_env, f"{f.pytest_args}{parallel_args}"


@click.command()
@click.option(
    "--target-env", envvar="QA_PTE_TARGET_ENV", default="", help="Target environment"
)
@click.option(
    "--pytest-args",
    envvar="QA_PTE_PYTEST_ARGS",
    default="",
    help="Additional arguments for pytest",
)
@click.option(
    "--config",
    envvar="QA_PTE_CONFIG",
    default="",
    help="Specify a pre-defined config to be used. If specified all other args are ignored.",
)
@click.option(
    "--list-configs", is_flag=True, help="List the known Test Execution Configs."
)
def trigger_pytest(target_env: str, pytest_args: str, config: str, list_configs: bool):
    """
    Wrapper for configuring test execution via pytest.

    Note:
    If using the --config option you can specify '_X' after the config identifier
    in order to achieve parallel test execution.
    E.g.
    # instead of
    $ execute-pytest --config Internal_Tests
    # you can use
    $ execute-pytest --config Internal_Tests_X

    """
    if list_configs:
        print(PREDEFINED_CONFIGS)
        return

    if config:
        # config overwrites any supplied value in the args
        _target_env, _pytest_args = config_lookup(config)
        if not target_env:
            # if no override target_env is supplied then use config value
            target_env = _target_env
        if pytest_args:
            # if override pytest args are supplied then merge with config
            pytest_args = f"{_pytest_args} {pytest_args}"
        else:
            # if no override pytest args are supplied use config else merge
            pytest_args = _pytest_args

    if not config and not target_env:
        raise TargetEnvironmentNotSpecified()

    print(f"Supplied {pytest_args=}")
    print(f"Supplied {target_env=}")
    if target_env.lower() != "internal":
        os.environ["ENV_FOR_DYNACONF"] = target_env
    full_pytest_args = [TESTS_DIR]
    if pytest_args:
        full_pytest_args.extend(pytest_args.split(" "))
    print(f"Complete pytest args: {full_pytest_args}")
    return_code = pytest.main(full_pytest_args)
    print(f"Test Execution {return_code=} [{int(return_code)}]")
    sys.exit(return_code)
