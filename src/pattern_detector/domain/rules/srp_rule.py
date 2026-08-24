"""Go Single Responsibility Principle (SRP) Rule (God Struct)."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class SingleResponsibilityRule(BasePatternRule):
    """Detects God Structs in Go."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.SINGLE_RESPONSIBILITY

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for st in model.all_structs():
            method_count = len(st.methods)
            field_count = len(st.fields)

            if method_count >= 15 or (method_count >= 10 and field_count >= 12):
                evidences = [
                    Evidence(
                        description=f"SRP Violation (God Struct): Struct '{st.name}' has {method_count} methods and {field_count} fields, indicating mixed domain responsibilities",
                        weight=0.85,
                        rule_code="SRP_GOD_STRUCT",
                        location=st.location,
                    )
                ]
                det = self._create_detection(
                    target_name=st.name,
                    target_kind="god_struct",
                    evidences=evidences,
                    location=st.location,
                )
                detections.append(det)

        return detections
