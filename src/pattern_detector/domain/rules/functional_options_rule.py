"""Go Functional Options Pattern Rule (Idiomatic Creational Pattern)."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class FunctionalOptionsRule(BasePatternRule):
    """Detects Functional Options Pattern in Go (type Option func(*Config) or type Option interface { apply(*Config) })."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.FUNCTIONAL_OPTIONS

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        # 1. Look for type Option func(*Target)
        option_aliases = [
            alias for alias in model.all_type_aliases()
            if alias.is_func_type and ("Option" in alias.name or "Opt" in alias.name or "ConfigFunc" in alias.name or "optionFunc" in alias.name)
        ]

        for opt in option_aliases:
            evidences = [
                Evidence(
                    description=f"Type '{opt.name}' ({opt.underlying_type}) defines idiomatic Go Functional Option signature for clean struct configuration",
                    weight=0.60,
                    rule_code="FUNCTIONAL_OPTION_TYPE_DEF",
                    location=opt.location,
                )
            ]

            # Look for With* builder option functions returning this Option type
            with_funcs = [
                fn for fn in model.all_functions()
                if (fn.name.startswith("With") or fn.name.startswith("Wrap")) and (opt.name in fn.return_type_str or "func(" in fn.return_type_str)
            ]
            if with_funcs:
                evidences.append(
                    Evidence(
                        description=f"Provides {len(with_funcs)} option generator function(s) ({', '.join(f.name for f in with_funcs[:3])})",
                        weight=0.50,
                        rule_code="FUNCTIONAL_OPTION_WITH_FUNCS",
                        location=with_funcs[0].location or opt.location,
                    )
                )

            # Look for constructor function accepting variadic opts ...Option
            constructors = [
                fn for fn in model.all_functions()
                if any(p[1] == f"...{opt.name}" or p[1] == f"...func(" for p in fn.params)
            ]
            if constructors:
                evidences.append(
                    Evidence(
                        description=f"Constructor '{constructors[0].name}' accepts variadic functional options ({constructors[0].params[-1][0]} ...{opt.name})",
                        weight=0.45,
                        rule_code="FUNCTIONAL_OPTION_CONSTRUCTOR",
                        location=constructors[0].location or opt.location,
                    )
                )

            det = self._create_detection(
                target_name=opt.name,
                target_kind="functional_option_type",
                evidences=evidences,
                location=opt.location,
            )
            detections.append(det)

        # 2. Look for Option Interface (Uber Option style: type Option interface { apply(*Logger) })
        for iface in model.all_interfaces():
            if iface.name in ("Option", "LoggerOption", "ServerOption", "ClientOption") or (iface.name.endswith("Option") and any(m.lower().startswith("apply") for m in iface.methods)):
                evidences = [
                    Evidence(
                        description=f"Interface '{iface.name}' defines idiomatic Option interface with application hook(s) ({', '.join(iface.methods.keys())})",
                        weight=0.75,
                        rule_code="FUNCTIONAL_OPTION_INTERFACE",
                        location=iface.location,
                    )
                ]
                with_funcs = [
                    fn for fn in model.all_functions()
                    if (fn.name.startswith("With") or fn.name.startswith("Wrap") or fn.name.startswith("Fields")) and iface.name in fn.return_type_str
                ]
                if with_funcs:
                    evidences.append(
                        Evidence(
                            description=f"Provides {len(with_funcs)} option generator function(s) ({', '.join(f.name for f in with_funcs[:3])})",
                            weight=0.45,
                            rule_code="FUNCTIONAL_OPTION_WITH_FUNCS",
                            location=with_funcs[0].location or iface.location,
                        )
                    )
                det = self._create_detection(
                    target_name=iface.name,
                    target_kind="functional_option_interface",
                    evidences=evidences,
                    location=iface.location,
                )
                detections.append(det)

        return detections
