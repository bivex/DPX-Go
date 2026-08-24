"""Domain Code Model for Go (Golang) Static Architecture and Pattern Analysis."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from typing import Any, Sequence

from pattern_detector.domain.value_objects import SourceLocation


@dataclass
class FieldModel:
    """Represents a struct field in Go."""

    name: str
    type_str: str
    tag: str = ""
    is_embedded: bool = False
    location: SourceLocation | None = None


@dataclass
class FunctionModel:
    """Represents a standalone function or method in Go."""

    name: str
    receiver_name: str | None = None
    receiver_type: str | None = None  # e.g. "*Server", "Server", None
    is_pointer_receiver: bool = False
    params: list[tuple[str, str]] = field(default_factory=list)  # [(param_name, param_type), ...]
    return_types: list[str] = field(default_factory=list)
    body: str = ""
    calls: list[str] = field(default_factory=list)
    doc: str = ""
    cyclomatic_complexity: int = 1
    has_goroutine: bool = False
    has_channel_op: bool = False
    location: SourceLocation | None = None

    @property
    def is_method(self) -> bool:
        return self.receiver_type is not None

    @property
    def return_type_str(self) -> str:
        if not self.return_types:
            return "()"
        if len(self.return_types) == 1:
            return self.return_types[0]
        return f"({', '.join(self.return_types)})"


@dataclass
class StructModel:
    """Represents a Go struct definition (`type Server struct { ... }`)."""

    name: str
    package: str
    fields: list[FieldModel] = field(default_factory=list)
    embedded_types: list[str] = field(default_factory=list)
    methods: dict[str, FunctionModel] = field(default_factory=dict)
    doc: str = ""
    location: SourceLocation | None = None

    @property
    def field_names(self) -> list[str]:
        return [f.name for f in self.fields]

    @property
    def field_types(self) -> list[str]:
        return [f.type_str for f in self.fields]


@dataclass
class InterfaceMethodModel:
    """Represents a method declared in a Go interface."""

    name: str
    params: list[tuple[str, str]] = field(default_factory=list)
    return_types: list[str] = field(default_factory=list)
    location: SourceLocation | None = None


@dataclass
class InterfaceModel:
    """Represents a Go interface definition (`type Reader interface { ... }`)."""

    name: str
    package: str
    methods: dict[str, InterfaceMethodModel] = field(default_factory=dict)
    embedded_interfaces: list[str] = field(default_factory=list)
    doc: str = ""
    location: SourceLocation | None = None


@dataclass
class TypeAliasModel:
    """Represents a Go custom type definition (`type Option func(*Server)` or `type State int`)."""

    name: str
    package: str
    underlying_type: str
    is_func_type: bool = False
    location: SourceLocation | None = None


@dataclass
class FileModel:
    """Represents a single Go source file (.go)."""

    package: str
    file_path: str
    imports: list[str] = field(default_factory=list)
    structs: dict[str, StructModel] = field(default_factory=dict)
    interfaces: dict[str, InterfaceModel] = field(default_factory=dict)
    type_aliases: dict[str, TypeAliasModel] = field(default_factory=dict)
    functions: dict[str, FunctionModel] = field(default_factory=dict)
    raw_source: str = ""
    location: SourceLocation | None = None


@dataclass
class CodeModel:
    """Aggregated semantic domain model of a Go project or module."""

    files: dict[str, FileModel] = field(default_factory=dict)
    project_path: str = ""

    # -------------------------------------------------------------------------
    # Aggregations
    # -------------------------------------------------------------------------

    def all_structs(self) -> list[StructModel]:
        res = []
        for f in self.files.values():
            res.extend(f.structs.values())
        return res

    def all_interfaces(self) -> list[InterfaceModel]:
        res = []
        for f in self.files.values():
            res.extend(f.interfaces.values())
        return res

    def all_type_aliases(self) -> list[TypeAliasModel]:
        res = []
        for f in self.files.values():
            res.extend(f.type_aliases.values())
        return res

    def all_functions(self) -> list[FunctionModel]:
        seen: set[int] = set()
        res: list[FunctionModel] = []

        def _add(fn: FunctionModel) -> None:
            obj_id = id(fn)
            if obj_id not in seen:
                seen.add(obj_id)
                res.append(fn)

        for f in self.files.values():
            for fn in f.functions.values():
                _add(fn)
            for st in f.structs.values():
                for m in st.methods.values():
                    _add(m)
        return res

    def find_struct(self, name: str) -> StructModel | None:
        clean = name.lstrip("*")
        for st in self.all_structs():
            if st.name == clean:
                return st
        return None

    def find_interface(self, name: str) -> InterfaceModel | None:
        for iface in self.all_interfaces():
            if iface.name == name:
                return iface
        return None

    def find_type_alias(self, name: str) -> TypeAliasModel | None:
        for alias in self.all_type_aliases():
            if alias.name == name:
                return alias
        return None

    # -------------------------------------------------------------------------
    # Dependency Graph & Circular Dependency Detection
    # -------------------------------------------------------------------------

    def build_package_dependency_graph(self) -> dict[str, set[str]]:
        graph: dict[str, set[str]] = {}
        pkg_to_files: dict[str, list[FileModel]] = {}

        for f in self.files.values():
            pkg_to_files.setdefault(f.package, []).append(f)
            if f.package not in graph:
                graph[f.package] = set()

        for pkg, files in pkg_to_files.items():
            for f in files:
                for imp in f.imports:
                    # Clean import path e.g. "github.com/foo/bar/pkg" -> "pkg"
                    imp_pkg = imp.strip('"').split("/")[-1]
                    if imp_pkg in graph and imp_pkg != pkg:
                        graph[pkg].add(imp_pkg)

        return graph

    def find_circular_dependencies(self, max_depth: int = 8, max_cycles: int = 50) -> list[list[str]]:
        graph = self.build_package_dependency_graph()
        cycles: list[list[str]] = []
        visited: set[str] = set()

        def _dfs(current: str, path: list[str], path_set: set[str]) -> None:
            if len(cycles) >= max_cycles:
                return
            path.append(current)
            path_set.add(current)

            for neighbor in sorted(graph.get(current, set())):
                if neighbor == path[0] and len(path) > 1:
                    canonical = tuple(path)
                    rotations = [canonical[i:] + canonical[:i] for i in range(len(canonical))]
                    min_rot = list(min(rotations))
                    if min_rot not in cycles:
                        cycles.append(min_rot)
                elif neighbor not in path_set and neighbor not in visited and len(path) < max_depth:
                    _dfs(neighbor, path, path_set)

            path.pop()
            path_set.remove(current)

        for node in sorted(graph.keys()):
            _dfs(node, [], set())
            visited.add(node)

        return cycles
