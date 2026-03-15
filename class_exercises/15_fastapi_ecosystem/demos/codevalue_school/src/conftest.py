import os

from src.secrets_accessor import MODE_ENV_VAR, RunMode

os.environ[MODE_ENV_VAR] = RunMode.TEST.value
