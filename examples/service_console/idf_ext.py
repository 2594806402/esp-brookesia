from typing import Any
import subprocess, sys
import os
from pathlib import Path
import shutil
import importlib.util

IDF_PATH = os.getenv("IDF_PATH", "")

def load_from_path(file_path, module_name=None):
    """file_path: any .py file; returns the loaded module object"""
    module_name = module_name or file_path.stem
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f'Failed to create spec for {file_path}')
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod

def action_extensions(base_actions: dict, project_path: str) -> dict:

    bmgr_path = Path(project_path) / "managed_components" / "espressif__esp_board_manager"
    

    # 检查是否正在执行 update-dependencies，避免递归
=======
    # Check whether update-dependencies is being executed to avoid recursion
>>>>>>> cf7f07e9ddf404aaa4e940d30d0158b7e5d22dff
    is_updating_deps = os.getenv("_IDF_EXT_UPDATING_DEPS") == "1" or \
                       (len(sys.argv) > 1 and sys.argv[1] == "update-dependencies")

    if not bmgr_path.exists() and not is_updating_deps:

        # 设置环境变量标记，避免递归
        os.environ["_IDF_EXT_UPDATING_DEPS"] = "1"
        try:
            # 使用 idf.py update-dependencies，但通过环境变量避免递归
=======
        # Set an environment flag to avoid recursion
        os.environ["_IDF_EXT_UPDATING_DEPS"] = "1"
        try:
            # Use idf.py update-dependencies while preventing recursion via the env flag
>>>>>>> cf7f07e9ddf404aaa4e940d30d0158b7e5d22dff
            result = subprocess.run(
                [sys.executable, f"{IDF_PATH}/tools/idf.py", "update-dependencies"],
                env={**os.environ, "_IDF_EXT_UPDATING_DEPS": "1"},
                cwd=project_path
            )
            if result.returncode != 0:
                print(f"Warning: Failed to update dependencies. Return code: {result.returncode}")
        finally:

            # 清除环境变量标记
=======
            # Clear the environment flag
>>>>>>> cf7f07e9ddf404aaa4e940d30d0158b7e5d22dff
            os.environ.pop("_IDF_EXT_UPDATING_DEPS", None)

    def esp_gen_bmgr_config_callback(target_name: str, ctx, args, **kwargs) -> None:
        raise Exception("should not be called")

    if not bmgr_path.exists():
        # Define a fake action to avoid error
        esp_actions = {
            "actions": {
                "gen-bmgr-config": {
                    "callback": esp_gen_bmgr_config_callback,
                    "options": [],
                    "short_help": "Generate ESP Board Manager configuration files",
                },
            }
        }
        return esp_actions
    else:

        # shutil.rmtree("components/gen_bmgr_codes", ignore_errors=True)
=======
>>>>>>> cf7f07e9ddf404aaa4e940d30d0158b7e5d22dff
        file_path = bmgr_path / "idf_ext.py"
        bmgr_config = load_from_path(file_path)
        return bmgr_config.action_extensions(base_actions, project_path)
