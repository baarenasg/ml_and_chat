import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Union


@lru_cache()
def load_json_file(file_path: Union[str, Path]) -> Dict[str, Any]:
    """Función para cargar un json.

    :param file_path: String con el path del archivo
    :return:
    """
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    raise FileNotFoundError(f"File {file_path} not found")
