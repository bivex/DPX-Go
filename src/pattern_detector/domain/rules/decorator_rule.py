"""Go Decorator / Middleware Pattern Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class DecoratorPatternRule(BasePatternRule):
    """Detects Decorator / Middleware Pattern in Go."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.DECORATOR

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for st in model.all_structs():
            evidences: list[Evidence] = []
            name_lower = st.name.lower()

            if "decorator" in name_lower or "wrapper" in name_lower or "middleware" in name_lower or "logging" in name_lower or "metrics" in name_lower:
                evidences.append(
                    Evidence(
                        description=f"Struct '{st.name}' follows Decorator / Middleware naming convention",
                        weight=0.35,
                        rule_code="DECORATOR_NAMING",
                        location=st.location,
                    )
                )

            # Wraps next / inner interface field
            next_fields = [
                f for f in st.fields
                if f.name in ("next", "inner", "wrapped", "handler", "delegate", "service")
            ]
            if next_fields:
                evidences.append(
                    Evidence(
                        description=f"Wraps inner component '{next_fields[0].name}: {next_fields[0].type_str}' to decorate behavior",
                        weight=0.50,
                        rule_code="DECORATOR_WRAPS_COMPONENT",
                        location=st.location,
                    )
                )

            if evidences:
                det = self._create_detection(
                    target_name=st.name,
                    target_kind="decorator_struct",
                    evidences=evidences,
                    location=st.location,
                )
                if det.confidence.score >= 0.50:
                    detections.append(det)

        return detections
