# To Do

1. Remove `shell=True` and build argv lists instead in `ssh_audio_play/play.py`.
   The playback command is currently assembled as a shell string and executed with `subprocess.Popen(..., shell=True)`, which is fragile and harder to secure. This matters most in remote mode because `sox | ssh | play` is composed from user-influenced values.

2. Validate time arguments in `ssh_audio_play/play.py`.
   `end - start` can go negative, and `start` and `duration` are accepted without range checks. Add a small validator so invalid `trim` commands fail early with clear errors.

3. Add tests around command construction and config loading.
   Focus on local vs remote command generation, missing env vars, invalid mode, and time slicing behavior in `ssh_audio_play/play.py` and `ssh_audio_play/ssh_audio_config.py`.

4. Improve packaging metadata in `pyproject.toml`.
   Add common fields like `requires-python`, `readme`, `license`, authors, and useful project URLs to make installation and publishing cleaner.

5. Add a CLI entry point.
   Provide a console script such as `ssh-audio-play /path/file.wav --start 1.2 --end 3.8` so the tool is usable directly from the shell instead of only through Python.

6. Tighten the README.
   Clarify setup steps, correct the SSH port example, add explicit local vs remote examples, and document that both ends need `sox` and `play`. Also simplify the install URLs.

7. Reconsider version bumping on every commit.
   The hook works, but auto-bumping package version per commit creates noisy history and versions that do not map cleanly to releases. A tag- or release-driven versioning flow is usually cleaner.
