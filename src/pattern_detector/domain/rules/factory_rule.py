"""Go Factory Method Rule (Constructor Functions)."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class FactoryMethodRule(BasePatternRule):
    """Detects Factory constructor functions in Go (New..., NewFromConfig)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.FACTORY_METHOD

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for fn in model.all_functions():
            # Top-level constructor function starting with New or Open
            if not fn.is_method and (fn.name.startswith("New") or fn.name.startswith("Open")):
                if fn.return_types and any(t.startswith("*") or t[0].isupper() for t in fn.return_types):
                    evidences = [
                        Evidence(
                            description=f"Factory constructor function '{fn.name}()' encapsulates instantiation of '{fn.return_type_str}'",
                            weight=0.65,
                            rule_code="FACTORY_METHOD_CONSTRUCTOR",
                            location=fn.location,
                        )
                    ]
                    if len(fn.params) >= 1:
                        evidences.append(
                            Evidence(
                                description=f"Encapsulates parameterized construction across {len(fn.params)} input parameter(s)",
                                weight=0.30,
                                rule_code="FACTORY_METHOD_PARAMETERIZED",
                                location=fn.location,
                            )
                        )

                    det = self._create_detection(
                        target_name=fn.name,
                        target_kind="factory_function",
                        evidences=evidences,
                        location=fn.location,
                    )
                    detections.append(det)

        return detections
