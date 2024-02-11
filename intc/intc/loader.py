# Copyright the author(s) of intc.
#
# This source code is licensed under the Apache license found in the
# LICENSE file in the root directory of this source tree.

import copy
import json
import os
from typing import Dict, List, Union

import hjson
import yaml

import intc.share as G
from intc.exceptions import NameError, RepeatRegisterError
from intc.register import cregister, ic_help, ic_repo


def load_submodule(cur_dir: str = None):
    if G.LOAD_SUBMODULE_DONE:
        return
    G.LOAD_SUBMODULE_DONE = True
    if not cur_dir:
        cur_dir = os.getcwd()
    intc_rc_config_path = ""
    for meta_config in [".intc.json", ".intc.jsonc"]:
        if os.path.isfile(os.path.join(cur_dir, meta_config)):
            intc_rc_config_path = os.path.join(cur_dir, meta_config)
            break
    if not intc_rc_config_path:
        return
    intc_rc_config = hjson.load(open(intc_rc_config_path, "r"), object_pairs_hook=dict)
    modules = intc_rc_config.get("module", [])
    loader = Loader(ignore_error=True)
    for module in modules:
        module_path = os.path.join(cur_dir, module)
        loader.load_files(module_path)


class Loader(object):
    """load config from repo paths"""

    def __init__(self, ignore_error=False):
        super(Loader, self).__init__()
        self.ignore_error = ignore_error
        self.stashed = {}

    def resolve(self):
        """resolve dependency
        Returns:
            None
        """

        while self.stashed:
            circle_flag = True
            for key in self.stashed:
                if self.stashed[key]["base"] in ic_repo:
                    self.store(key, self.stashed[key])
                    del self.stashed[key]
                    circle_flag = False
                    break
            if circle_flag:
                raise NameError(f"Unresolved dependency {self.stashed}")

    def store(self, key: tuple, config: dict):
        """
        Args:
            config (TODO): TODO

        Returns: TODO

        """
        ic_repo[key] = copy.deepcopy(config["config"])
        base_help = copy.deepcopy(ic_help.get(config["base"], {}))
        base_help["inter_files"] = base_help.get("inter_files", []) + config["path"]
        ic_help[key] = base_help

    def stash(self, config: Dict, file_path, base: tuple, key: tuple):
        """stash the config to the repo, and wait for resolve the dependency
        Returns:
            None
        """
        assert (
            key not in ic_repo and key not in self.stashed
        ), f"Module {key} has been registered"
        if base not in ic_repo:
            self.stashed[key] = {"config": config, "path": [file_path], "base": base}
        else:
            self.store(key, {"config": config, "path": [file_path], "base": base})
        return None

    @staticmethod
    def get_base(config):
        """

        Args:
            config:
                The config to save.

        Returns:
            module_base
        """
        module_name = ""
        if not config:
            return module_name
        assert "_base" in config, f"Invalid config {config}"
        module_name = config.get("_base", None) or ""
        return module_name

    @staticmethod
    def get_key(path):
        """
        Args:
            path:
                The path which locates the config file.
        Returns:
            module_type, module_name
        """

        module_type, module_name = "", ""
        if not path:
            return module_type, module_name
        path = ".".join(path.split("/")[-1].split(".")[:-1])
        keys = path.split("@")
        assert len(keys) <= 2, f"Invalid module name {path}"
        module_type = keys[0]
        if len(keys) == 2:
            module_name = keys[1]
        return module_type, module_name

    def load_files(self, config_dir: str, exclude: List[str] = []):
        """Recursively load config from config_dir

        Args:
            config_dir:
                The config directory that contains the config files.

        Kwargs:
            exclude:
                The list of files to exclude from loading.

        Returns:
            None
        """

        for root, dirs, files in os.walk(config_dir):
            for file in files:
                try:
                    if file.startswith("_") or file in exclude:
                        continue

                    file_path = os.path.join(root, file)
                    file_ext = os.path.splitext(file)[1].lower()
                    data = None

                    # Load JSON file
                    if file_ext == ".json":
                        data = self.load_json(file_path)

                    # Load HJSON file
                    elif file_ext == ".hjson" or file_ext == ".jsonc":
                        data = self.load_hjson(file_path)

                    # Load YAML file
                    elif file_ext == ".yaml" or file_ext == ".yml":
                        data = self.load_yaml(file_path)
                    if data:
                        key_module_type, key_module_name = self.get_key(file_path)
                        base_module_name = self.get_base(data)
                        self.stash(
                            data,
                            file_path,
                            (key_module_type, base_module_name),
                            (key_module_type, key_module_name),
                        )
                except Exception as e:
                    if not self.ignore_error:
                        raise e
        return

    @staticmethod
    def load_json(file_path: str) -> Dict:
        """Load JSON file"""
        with open(file_path, "r") as f:
            data = json.load(f)
        return data

    @staticmethod
    def load_hjson(file_path: str) -> Dict:
        """Load HJSON/jsonc file"""
        with open(file_path, "r") as f:
            data = hjson.load(f)
        return data

    @staticmethod
    def load_yaml(file_path: str) -> Dict:
        """Load YAML file"""
        with open(file_path, "r") as f:
            data = yaml.safe_load(f)
        return data
