"""Install built manuals into the user's Info directory."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

from .config import BUILD, INFO_DIR


def install(names: list[str], info_dir: Path = INFO_DIR, log=print) -> bool:
    """Copy build/info/<name>.info into info_dir and register it in the dir
    file. A manual that fails to install leaves the previous copy in place."""
    info_dir.mkdir(parents=True, exist_ok=True)
    ok = True
    for name in names:
        src = BUILD / "info" / f"{name}.info"
        dest = info_dir / f"{name}.info"
        if not src.exists():
            log(f"{name}: not built, skipping")
            ok = False
            continue
        if dest.exists():
            # Drop the old dir entry (its category may differ from ours).
            subprocess.run(
                ["install-info", "--delete", f"--info-dir={info_dir}", str(dest)],
                capture_output=True, text=True,
            )
        for old in list(info_dir.glob(f"{name}.info-*")) + list(info_dir.glob(f"{name}.info.gz")):
            old.unlink()  # split or compressed copies from earlier installs
        tmp = dest.with_name(f".{name}.info.tmp")
        shutil.copyfile(src, tmp)
        os.replace(tmp, dest)
        r = subprocess.run(
            ["install-info", f"--info-dir={info_dir}", str(dest)],
            capture_output=True, text=True,
        )
        if r.returncode != 0:
            log(f"{name}: install-info failed: {r.stderr.strip()}")
            ok = False
            continue
        log(f"{name}: installed {dest} ({dest.stat().st_size / 1e6:.1f} MB)")
    return ok
