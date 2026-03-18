import os

import decouple

config = decouple.AutoConfig(search_path=".")

ENV_PREFIX = "SSH_AUDIO_PLAY_"
UNSET = object()
LEGACY_ENV_KEYS = {
    "MODE": "AUDIO_MODE",
    "LOCAL_USER": "AUDIO_LOCAL_USER",
    "SSH_PORT": "AUDIO_SSH_PORT",
    "REMOTE_SOX": "AUDIO_REMOTE_SOX",
    "LOCAL_PLAY": "AUDIO_LOCAL_PLAY",
}


def _env_keys(key):
    return [f"{ENV_PREFIX}{key}", LEGACY_ENV_KEYS.get(key)]


def _get_config_value(key, *, cast=None, default=UNSET):
    for env_key in _env_keys(key):
        if not env_key:
            continue
        value = os.getenv(env_key)
        if value is not None:
            return cast(value) if cast else value

    for env_key in _env_keys(key):
        if not env_key:
            continue
        try:
            if default is UNSET:
                return config(env_key, cast=cast)
            return config(env_key, cast=cast, default=default)
        except decouple.UndefinedValueError:
            continue

    if default is not UNSET:
        return default

    raise decouple.UndefinedValueError(key)


def get_audio_mode():
    mode = _get_config_value("MODE", default="remote")

    if mode not in {"remote", "local"}:
        raise RuntimeError(
            f"AUDIO_MODE must be 'remote' or 'local', got '{mode}'"
        )
    return mode


def require(keys):
    missing = []
    values = {}

    for key in keys:
        try:
            values[key] = _get_config_value(key)
        except decouple.UndefinedValueError:
            missing.append(key)

    if missing:
        env_keys = ", ".join(f"{ENV_PREFIX}{key}" for key in missing)
        raise RuntimeError(
            "Missing audio configuration:\n"
            + "\n".join(f"  - {ENV_PREFIX}{k}" for k in missing)
            + f"\n\nSet them in the OS environment or in a .env file ({env_keys}). See env.example."
        )

    return values


def get_optional(key, *, cast=None, default=None):
    return _get_config_value(key, cast=cast, default=default)
