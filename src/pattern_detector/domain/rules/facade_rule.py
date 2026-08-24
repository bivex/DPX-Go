"""Go Facade Pattern Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class FacadePatternRule(BasePatternRule):
    """Detects Facade Pattern in Go."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.FACADE

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for st in model.all_structs():
            evidences: list[Evidence] = []
            name_lower = st.name.lower()

            if name_lower.endswith("facade") or name_lower.endswith("client") or name_lower.endswith("engine") or name_lower.endswith("service"):
                evidences.append(
                    Evidence(
                        description=f"Struct '{st.name}' follows Facade / High-Level Client naming convention",
                        weight=0.40,
                        rule_code="FACADE_NAMING",
                        location=st.location,
                    )
                )

            subsystems = [f for f in st.fields if f.type_str.startswith("*") or f.type_str[0].isupper()]
            if len(subsystems) >= 3:
                evidences.append(
                    Evidence(
                        description=f"Aggregates {len(subsystems)} subsystem services ({', '.join(f.name for f in subsystems[:3])}) behind unified API",
                        weight=0.45,
                        rule_code="FACADE_AGGREGATES_SUBSYSTEMS",
                        location=st.location,
                    )
                )

            if evidences:
                det = self._create_detection(
                    target_name=st.name,
                    target_kind="facade_struct",
                    evidences=evidences,
                    location=st.location,
                )
                if det.confidence.score >= 0.50:
                    detections.append(det)

        return detections
