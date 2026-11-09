"""Project paths and source definitions."""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(os.environ.get("CLAUDE_INFO_ROOT", Path(__file__).resolve().parents[2]))
MIRROR = ROOT / "mirror"
BUILD = ROOT / "build"
STATE = ROOT / ".state"
INFO_DIR = Path(
    os.environ.get("CLAUDE_INFO_INSTALL_DIR", Path.home() / ".local/share/info")
)


@dataclass(frozen=True)
class Manual:
    name: str
    title: str
    description: str
    prefixes: tuple[str, ...]


@dataclass(frozen=True)
class Source:
    id: str
    name: str
    base: str
    index: str | None = None
    sitemap: str | None = None
    index_start: str | None = None
    index_drop: tuple[str, ...] = ()
    exclude: tuple[str, ...] = ()
    derive_from: str | None = None
    derive_prefix: str = ""
    manuals: tuple[Manual, ...] = field(default_factory=tuple)

    @property
    def mirror(self) -> Path:
        return MIRROR / self.id

    @property
    def pages_dir(self) -> Path:
        return self.mirror / "pages"

    def manual_for(self, path: str) -> Manual:
        for manual in self.manuals:
            if any(path.startswith(p) for p in manual.prefixes):
                return manual
        raise ValueError(f"{self.id}: no manual matches {path!r}")


def load_sources(path: Path | None = None) -> list[Source]:
    data = tomllib.loads((path or ROOT / "sources.toml").read_text())
    sources = []
    for s in data["source"]:
        manuals = tuple(
            Manual(m["name"], m["title"], m["description"], tuple(m["prefixes"]))
            for m in s["manual"]
        )
        sources.append(
            Source(
                id=s["id"],
                name=s["name"],
                base=s["base"],
                index=s.get("index"),
                sitemap=s.get("sitemap"),
                index_start=s.get("index_start"),
                index_drop=tuple(s.get("index_drop", ())),
                exclude=tuple(s.get("exclude", ())),
                derive_from=s.get("derive_from"),
                derive_prefix=s.get("derive_prefix", ""),
                manuals=manuals,
            )
        )
    return sources

# Pandoc reader for normalized pages. CommonMark matches the indentation rules
# of the upstream MDX; extensions that would reinterpret literal text ($ prices,
# ~approximations, @mentions, :emoji:, smart quotes) are turned off.
PANDOC_READER = (
    "commonmark_x-smart-subscript-superscript-tex_math_dollars"
    "-yaml_metadata_block-implicit_header_references-emoji"
)

# Width of the generated Info text.
FILL_COLUMN = 78
