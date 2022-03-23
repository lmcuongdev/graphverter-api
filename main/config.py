import os.path
from importlib import import_module
from typing import Type

from config.base import BaseConfig

env = os.getenv("ENVIRONMENT", "local")
config_file = f"config/{env}.py"
if not os.path.isfile(config_file):
    env = "local"

config_name = f"config.{env}"

module = import_module(config_name)

config: Type[BaseConfig] = module.Config
config.ENV = env
