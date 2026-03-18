import os

import decouple

config = decouple.AutoConfig(search_path=".")

ENV_PREFIX = "SSH_AUDIO_PLAY_"
UNSET = object()


def _env_key(key):
    return f"{ENV_PREFIX}{key}"


def _get_config_value(key, *, cast=None, default=UNSET):
    env_key = _env_key(key)
    value = os.getenv(env_key)
    if value is not None:
        return cast(value) if cast else value

    try:
        kwargs = {}
        if cast is not None:
            kwargs["cast"] = cast
        if default is not UNSET:
            kwargs["default"] = default
        return config(env_key, **kwargs)
    except decouple.UndefinedValueError:
        pass

    if default is not UNSET:
        return default

    raise decouple.UndefinedValueError(key)


def get_audio_mode():
    mode = _get_config_value("MODE", default="remote")

    if mode not in {"remote", "local"}:
        raise RuntimeError(
            f"{ENV_PREFIX}MODE must be 'remote' or 'local', got '{mode}'"
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
