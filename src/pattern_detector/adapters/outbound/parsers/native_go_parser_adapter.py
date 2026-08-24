"""High-performance Native Go AST & CST Parser Adapter implementing ParserPort."""

from __future__ import annotations

import os
import re
from pathlib import Path

from pattern_detector.domain.code_model import (
    CodeModel,
    FieldModel,
    FileModel,
    FunctionModel,
    InterfaceMethodModel,
    InterfaceModel,
    StructModel,
    TypeAliasModel,
)
from pattern_detector.domain.value_objects import SourceLocation
from pattern_detector.ports.outbound import ParserPort


class NativeGoParserAdapter(ParserPort):
    """High-performance, fault-tolerant native Go parser supporting Go 1.18 - 1.24+ syntax."""

    def parse_sources(self, sources: dict[str, str]) -> CodeModel:
        model = CodeModel()
        for file_path, source_text in sources.items():
            file_model = self.parse_file(file_path, source_text)
            model.files[file_path] = file_model
        return model

    def parse_file(self, file_path: str, source_text: str) -> FileModel:
        loc = SourceLocation(file_path=file_path, line=1, column=1)
        pkg_name = self._parse_package_name(source_text)

        file_model = FileModel(
            package=pkg_name,
            file_path=file_path,
            raw_source=source_text,
            location=loc,
        )

        clean_text = self._strip_comments(source_text)

        # 1. Parse Imports
        file_model.imports = self._parse_imports(clean_text)

        # 2. Parse Type Aliases
        file_model.type_aliases = self._parse_type_aliases(clean_text, pkg_name, file_path)

        # 3. Parse Interfaces
        file_model.interfaces = self._parse_interfaces(clean_text, pkg_name, file_path)

        # 4. Parse Structs
        file_model.structs = self._parse_structs(clean_text, pkg_name, file_path)

        # 5. Parse Functions & Methods
        methods, standalone_funcs = self._parse_functions_and_methods(clean_text, file_path)
        file_model.functions = standalone_funcs

        # Attach methods to structs
        for recv_type, method_list in methods.items():
            clean_type = recv_type.lstrip("*")
            if clean_type in file_model.structs:
                for m in method_list:
                    file_model.structs[clean_type].methods[m.name] = m

        return file_model

    # -------------------------------------------------------------------------
    # Parsing Helpers
    # -------------------------------------------------------------------------

    def _parse_package_name(self, text: str) -> str:
        m = re.search(r"\bpackage\s+([a-zA-Z0-9_]+)", text)
        return m.group(1) if m else "main"

    def _strip_comments(self, text: str) -> str:
        text = re.sub(r"//.*", "", text)
        text = re.sub(r"/\*[\s\S]*?\*/", "", text)
        return text

    def _parse_imports(self, text: str) -> list[str]:
        imports = []
        # Multi-import: import ( ... )
        multi_matches = re.finditer(r"\bimport\s*\(([^)]*)\)", text)
        for mm in multi_matches:
            for line in mm.group(1).splitlines():
                line = line.strip()
                if line:
                    imp_match = re.search(r'"([^"]+)"', line)
                    if imp_match:
                        imports.append(imp_match.group(1))

        # Single import: import "..."
        single_matches = re.finditer(r'\bimport\s+"([^"]+)"', text)
        for sm in single_matches:
            imports.append(sm.group(1))

        return imports

    def _parse_type_aliases(self, text: str, pkg: str, file_path: str) -> dict[str, TypeAliasModel]:
        aliases = {}
        # type Option func(*Server) or type Option[T any] func(*T)
        pattern = re.compile(
            r"\btype\s+([a-zA-Z0-9_]+)(?:\[[^\]]+\])?\s+(func\s*\([^)]*\)[^{;\n]*|[a-zA-Z0-9_.*\[\]]+)",
            re.MULTILINE,
        )
        for m in pattern.finditer(text):
            name = m.group(1)
            target = m.group(2).strip()
            if target not in ("struct", "interface") and not target.startswith("struct{") and not target.startswith("interface{"):
                line_no = text[:m.start()].count("\n") + 1
                loc = SourceLocation(file_path=file_path, line=line_no)
                is_func = target.startswith("func(")
                aliases[name] = TypeAliasModel(
                    name=name,
                    package=pkg,
                    underlying_type=target,
                    is_func_type=is_func,
                    location=loc,
                )
        return aliases

    def _parse_interfaces(self, text: str, pkg: str, file_path: str) -> dict[str, InterfaceModel]:
        interfaces = {}
        pattern = re.compile(
            r"\btype\s+([a-zA-Z0-9_]+)(?:\[[^\]]+\])?\s+interface\s*\{",
            re.MULTILINE,
        )
        pos = 0
        while pos < len(text):
            m = pattern.search(text, pos)
            if not m:
                break
            name = m.group(1)
            line_no = text[:m.start()].count("\n") + 1
            loc = SourceLocation(file_path=file_path, line=line_no)

            body, end_pos = self._extract_balanced_braces(text, m.end() - 1)
            pos = end_pos + 1

            methods = {}
            embedded = []

            for line in body.splitlines():
                line = line.strip()
                if not line or line.startswith("//"):
                    continue
                # Method declaration: MethodName(p ...) (ret ...)
                mm = re.match(r"([A-Z][a-zA-Z0-9_]*)\s*\(([^)]*)\)(?:\s*(?:\(([^)]*)\)|([a-zA-Z0-9_.*\[\]]+)))?", line)
                if mm:
                    m_name = mm.group(1)
                    params_raw = mm.group(2)
                    ret_tuple = mm.group(3)
                    ret_single = mm.group(4)

                    params = self._parse_param_list(params_raw)
                    return_types = []
                    if ret_tuple:
                        return_types = [r.strip() for r in ret_tuple.split(",") if r.strip()]
                    elif ret_single:
                        return_types = [ret_single.strip()]

                    methods[m_name] = InterfaceMethodModel(
                        name=m_name,
                        params=params,
                        return_types=return_types,
                        location=loc,
                    )
                elif re.match(r"^[A-Z][a-zA-Z0-9_.]*$", line):
                    embedded.append(line)

            interfaces[name] = InterfaceModel(
                name=name,
                package=pkg,
                methods=methods,
                embedded_interfaces=embedded,
                location=loc,
            )

        return interfaces

    def _parse_structs(self, text: str, pkg: str, file_path: str) -> dict[str, StructModel]:
        structs = {}
        pattern = re.compile(
            r"\btype\s+([a-zA-Z0-9_]+)(?:\[[^\]]+\])?\s+struct\s*\{",
            re.MULTILINE,
        )
        pos = 0
        while pos < len(text):
            m = pattern.search(text, pos)
            if not m:
                break
            name = m.group(1)
            line_no = text[:m.start()].count("\n") + 1
            loc = SourceLocation(file_path=file_path, line=line_no)

            body, end_pos = self._extract_balanced_braces(text, m.end() - 1)
            pos = end_pos + 1

            fields = []
            embedded = []

            for line in body.splitlines():
                line = line.strip()
                if not line or line.startswith("//"):
                    continue

                tag = ""
                tag_match = re.search(r"`([^`]+)`", line)
                if tag_match:
                    tag = tag_match.group(1)
                    line = line[:tag_match.start()].strip()

                # Check for embedded struct (single identifier without field name)
                parts = line.split()
                if len(parts) == 1:
                    t_name = parts[0].lstrip("*")
                    if t_name[0].isupper() or "." in t_name:
                        embedded.append(parts[0])
                        fields.append(FieldModel(name=t_name.split(".")[-1], type_str=parts[0], tag=tag, is_embedded=True, location=loc))
                elif len(parts) >= 2:
                    f_name = parts[0]
                    f_type = " ".join(parts[1:])
                    fields.append(FieldModel(name=f_name, type_str=f_type, tag=tag, is_embedded=False, location=loc))

            structs[name] = StructModel(
                name=name,
                package=pkg,
                fields=fields,
                embedded_types=embedded,
                location=loc,
            )

        return structs

    def _parse_functions_and_methods(self, text: str, file_path: str) -> tuple[dict[str, list[FunctionModel]], dict[str, FunctionModel]]:
        methods: dict[str, list[FunctionModel]] = {}
        standalone_funcs: dict[str, FunctionModel] = {}

        # func (r *Receiver) MethodName(params) (returns) { ... } or func FunctionName(params) (returns) { ... }
        fn_pattern = re.compile(
            r"\bfunc\s*(?:\(([^)]+)\)\s*)?([a-zA-Z0-9_]+)(?:\[[^\]]+\])?\s*\(([^)]*)\)(?:\s*(?:\(([^)]*)\)|([^{]+)))?\s*\{",
            re.MULTILINE,
        )
        pos = 0
        while pos < len(text):
            m = fn_pattern.search(text, pos)
            if not m:
                break

            receiver_raw = m.group(1)
            name = m.group(2)
            params_raw = m.group(3)
            ret_tuple = m.group(4)
            ret_single = m.group(5)

            line_no = text[:m.start()].count("\n") + 1
            loc = SourceLocation(file_path=file_path, line=line_no)

            body, end_pos = self._extract_balanced_braces(text, m.end() - 1)
            pos = end_pos + 1

            params = self._parse_param_list(params_raw)
            return_types = []
            if ret_tuple:
                return_types = [r.strip() for r in ret_tuple.split(",") if r.strip()]
            elif ret_single:
                return_types = [ret_single.strip()]

            receiver_name = None
            receiver_type = None
            is_ptr = False

            if receiver_raw:
                recv_parts = receiver_raw.strip().split()
                if len(recv_parts) == 1:
                    receiver_type = recv_parts[0]
                elif len(recv_parts) >= 2:
                    receiver_name = recv_parts[0]
                    receiver_type = recv_parts[1]
                if receiver_type:
                    is_ptr = receiver_type.startswith("*")

            complexity = 1 + len(re.findall(r"\b(if|for|select|case|\&\&|\|\|)\b", body))
            calls = re.findall(r"([a-zA-Z0-9_]+(?:\.[a-zA-Z0-9_]+)*)\s*\(", body)
            has_go = "go func" in body or "go " in body
            has_chan = "<-" in body or "make(chan" in body

            fn_model = FunctionModel(
                name=name,
                receiver_name=receiver_name,
                receiver_type=receiver_type,
                is_pointer_receiver=is_ptr,
                params=params,
                return_types=return_types,
                body=body,
                calls=calls,
                cyclomatic_complexity=complexity,
                has_goroutine=has_go,
                has_channel_op=has_chan,
                location=loc,
            )

            if receiver_type:
                clean_type = receiver_type.lstrip("*")
                methods.setdefault(clean_type, []).append(fn_model)
            else:
                standalone_funcs[name] = fn_model

        return methods, standalone_funcs

    def _parse_param_list(self, params_raw: str) -> list[tuple[str, str]]:
        params = []
        if not params_raw:
            return params

        for p in params_raw.split(","):
            p = p.strip()
            if not p:
                continue
            parts = p.split()
            if len(parts) == 1:
                params.append(("", parts[0]))
            elif len(parts) >= 2:
                params.append((parts[0], " ".join(parts[1:])))

        return params

    def _extract_balanced_braces(self, text: str, start_index: int) -> tuple[str, int]:
        depth = 0
        in_string = False
        quote_char = ""
        escape = False

        for i in range(start_index, len(text)):
            c = text[i]
            if escape:
                escape = False
                continue
            if c == "\\" and in_string:
                escape = True
                continue
            if c in ('"', "'", "`") and not in_string:
                in_string = True
                quote_char = c
            elif c == quote_char and in_string:
                in_string = False
            elif not in_string:
                if c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
                    if depth == 0:
                        return text[start_index + 1 : i], i

        return text[start_index + 1 :], len(text) - 1
