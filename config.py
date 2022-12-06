from pathlib import Path

from dynaconf import Dynaconf

# Use environment Variable ENV_FOR_DYNACONF={env} to specify which Chetwood environment to target

CONFIG_DIR = Path("config")
EV_PREFIX = "CWQA_CONFIG"
ROOT_DIR = Path(__file__).resolve().parent
TESTS_DIR = ROOT_DIR / "tests"

settings = Dynaconf(
    envvar_prefix=EV_PREFIX,
    settings_files=[CONFIG_DIR / file for file in ["settings.yaml", ".secrets.yaml"]],
    environments=True,
    load_dotenv=True,
)
