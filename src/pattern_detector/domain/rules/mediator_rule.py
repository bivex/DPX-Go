"""Go Mediator Pattern Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class MediatorPatternRule(BasePatternRule):
    """Detects Mediator Pattern in Go."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.MEDIATOR

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for st in model.all_structs():
            evidences: list[Evidence] = []
            name_lower = st.name.lower()

            if name_lower.endswith("mediator") or name_lower.endswith("coordinator") or name_lower.endswith("dispatcher"):
                evidences.append(
                    Evidence(
                        description=f"Struct '{st.name}' follows Mediator / Dispatcher naming convention",
                        weight=0.45,
                        rule_code="MEDIATOR_NAMING",
                        location=st.location,
                    )
                )

            channel_maps = [
                f for f in st.fields
                if "map[" in f.type_str and ("chan" in f.type_str or "func(" in f.type_str or "*" in f.type_str)
            ]
            if channel_maps:
                evidences.append(
                    Evidence(
                        description=f"Maintains decoupled participant registry '{channel_maps[0].name}: {channel_maps[0].type_str}'",
                        weight=0.55,
                        rule_code="MEDIATOR_PARTICIPANTS_MAP",
                        location=st.location,
                    )
                )

            if evidences:
                det = self._create_detection(
                    target_name=st.name,
                    target_kind="mediator_struct",
                    evidences=evidences,
                    location=st.location,
                )
                if det.confidence.score >= 0.50:
                    detections.append(det)

        return detections
