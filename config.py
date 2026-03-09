"""Configuration loading utilities."""

from pathlib import Path

from omegaconf import OmegaConf

from models import AppConfig


def load_config(config_path: Path) -> AppConfig:
    """Load and validate application configuration.

    Args:
        config_path: Path to YAML configuration file.

    Returns:
        Validated AppConfig instance.
    """
    raw_conf = OmegaConf.load(config_path)
    return AppConfig.model_validate(OmegaConf.to_container(raw_conf))
