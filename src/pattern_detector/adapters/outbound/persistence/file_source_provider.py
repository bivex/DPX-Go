"""File-system based Go source code provider."""

from __future__ import annotations

import os
from pathlib import Path

from pattern_detector.ports.outbound import SourceProviderPort


class FileSourceProvider(SourceProviderPort):
    """Recursively retrieves Go source code files (.go) from disk."""

    DEFAULT_EXCLUDES = {
        ".git",
        "vendor",
        ".venv",
        "venv",
        "__pycache__",
        ".hg",
        ".svn",
        ".idea",
        ".vscode",
        "node_modules",
    }

    def get_sources(
        self,
        target_path: str,
        extensions: list[str] | None = None,
        exclude_dirs: list[str] | None = None,
    ) -> dict[str, str]:
        exts = extensions or [".go"]
        target = Path(target_path).resolve()
        sources: dict[str, str] = {}

        user_excludes = set(exclude_dirs or [])
        clean_user_excludes = {ex.strip("/\\") for ex in user_excludes if ex.strip("/\\")}

        if target.is_file():
            if any(str(target).endswith(ext) for ext in exts):
                sources[str(target)] = self._read_file(target)
            return sources

        if target.is_dir():
            for root, dirs, files in os.walk(target):
                dirs[:] = [
                    d
                    for d in dirs
                    if d not in self.DEFAULT_EXCLUDES
                    and d not in clean_user_excludes
                    and not any(ex == d or ex in f"{root}/{d}".split(os.sep) for ex in clean_user_excludes)
                ]

                try:
                    rel_parts = set(Path(root).resolve().relative_to(target).parts)
                    if any(ex in rel_parts for ex in clean_user_excludes):
                        continue
                except ValueError:
                    pass

                for file in files:
                    if any(file.endswith(ext) for ext in exts):
                        full_path = Path(root) / file
                        sources[str(full_path)] = self._read_file(full_path)

        return sources

    def _read_file(self, path: Path) -> str:
        try:
            return path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            return ""
