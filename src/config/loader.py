from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, MutableMapping, Optional

import yaml

from .models import AppConfig

DEFAULT_CANDIDATE_PATHS: list[Path] = [
    Path("./config.yaml"),
    Path("./config/settings.yaml"),
    Path.home() / ".config" / "lightbulbflow" / "config.yaml",
    Path("/etc/lightbulbflow/config.yaml"),
]


def find_config_path(explicit_path: Optional[str] = None) -> Optional[Path]:
    """
    Resolve the configuration file path using:
    1) explicit --config path
    2) $LBF_CONFIG environment variable
    3) common default locations
    Returns a Path if found, otherwise None.
    """
    if explicit_path:
        p = Path(explicit_path).expanduser()
        return p if p.is_file() else None

    env_path = os.getenv("LBF_CONFIG")
    if env_path:
        p = Path(env_path).expanduser()
        return p if p.is_file() else None

    for candidate in DEFAULT_CANDIDATE_PATHS:
        if candidate.is_file():
            return candidate
    return None


def _safe_load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)  # safe_load prevents executing arbitrary constructors
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError(f"Top-level YAML in {path} must be a mapping/object")
    return data


def _expand_env_vars(obj: Any) -> Any:
    """
    Recursively expand ${VAR} in strings using environment variables.
    """
    if isinstance(obj, str):
        return os.path.expandvars(obj)
    if isinstance(obj, list):
        return [_expand_env_vars(i) for i in obj]
    if isinstance(obj, dict):
        return {k: _expand_env_vars(v) for k, v in obj.items()}
    return obj


def _deep_merge(base: MutableMapping[str, Any], override: Mapping[str, Any]) -> MutableMapping[str, Any]:
    """
    Deep-merge two dict-like mappings. 'override' values take precedence.
    Lists are replaced (not merged) by default, which is predictable and safe.
    """
    for k, v in override.items():
        if k in base and isinstance(base[k], dict) and isinstance(v, Mapping):
            _deep_merge(base[k], v)
        else:
            base[k] = v
    return base


def _insert_nested(d: MutableMapping[str, Any], keys: Iterable[str], value: Any) -> None:
    curr = d
    *parents, last = list(keys)
    for k in parents:
        curr = curr.setdefault(k, {})
        if not isinstance(curr, dict):
            raise ValueError(f"Cannot nest into non-dict at {k}")
    curr[last] = value


def env_overrides(prefix: str = "LBF", delimiter: str = "__") -> dict:
    """
    Build a nested dict of overrides from environment variables.
    Example:
      LBF__SCRAPING__TIMEOUT=15
      LBF__OUTPUT__FORMAT=csv
    -> {"scraping": {"timeout": "15"}, "output": {"format": "csv"}}
    Values are kept as strings; Pydantic will coerce/validate types later.
    """
    result: dict[str, Any] = {}
    full_prefix = f"{prefix}{delimiter}"
    for env_key, env_val in os.environ.items():
        if not env_key.startswith(full_prefix):
            continue
        path_parts = env_key[len(full_prefix):].split(delimiter)
        # Normalize to lower_snake_case keys to match Pydantic fields
        norm_parts = [p.strip().lower() for p in path_parts if p.strip()]
        if not norm_parts:
            continue
        _insert_nested(result, norm_parts, env_val)
    return result


def load_config(
        config_path: Optional[str] = None,
        overrides: Optional[Mapping[str, Any]] = None,
        allow_missing: bool = True,
) -> AppConfig:
    """
    Load configuration with precedence:
    defaults (in code) < YAML file < environment variables < explicit overrides (e.g., CLI)
    - config_path: explicit path; if None, auto-discover
    - overrides: a mapping of explicit overrides to apply last
    - allow_missing: if False, raises if no config file is found
    """
    discovered = find_config_path(config_path)
    data: dict[str, Any] = {}

    if discovered:
        file_data = _safe_load_yaml(discovered)
        data = _expand_env_vars(file_data)
    elif not allow_missing:
        raise FileNotFoundError("No configuration file found and allow_missing=False")

    # Apply env var overrides like LBF__SCRAPING__TIMEOUT=15
    data = _deep_merge(data, env_overrides(prefix="LBF", delimiter="__"))

    # Apply final explicit overrides (e.g., from CLI flags mapped to nested dict)
    if overrides:
        data = _deep_merge(data, overrides)

    # Validate and coerce types using Pydantic
    return AppConfig.model_validate(data)
