import decouple


def get_audio_mode():
    mode = decouple.config("AUDIO_MODE", default="remote")

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
            values[key] = decouple.config(key)
        except decouple.UndefinedValueError:
            missing.append(key)

    if missing:
        raise RuntimeError(
            "Missing audio configuration:\n"
            + "\n".join(f"  - {k}" for k in missing)
            + "\n\nCreate a .env file (see .env.example)."
        )

    return values


def get_optional(key, *, cast=None, default=None):
    return decouple.config(key, cast=cast, default=default)

