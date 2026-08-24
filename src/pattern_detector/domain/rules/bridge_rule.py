"""Go Bridge Pattern Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class BridgePatternRule(BasePatternRule):
    """Detects Bridge Pattern in Go (struct decoupling abstraction from interface backend)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.BRIDGE

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for st in model.all_structs():
            bridge_fields = [
                f for f in st.fields
                if f.name in ("driver", "backend", "platform", "provider", "transport")
                and (f.type_str[0].isupper() or f.type_str.startswith("driver.") or f.type_str.startswith("backend."))
            ]
            if bridge_fields:
                evidences = [
                    Evidence(
                        description=f"Struct '{st.name}' decouples abstraction from implementation via '{bridge_fields[0].name}: {bridge_fields[0].type_str}'",
                        weight=0.65,
                        rule_code="BRIDGE_IMPLEMENTATION_FIELD",
                        location=st.location,
                    )
                ]
                det = self._create_detection(
                    target_name=st.name,
                    target_kind="bridge_struct",
                    evidences=evidences,
                    location=st.location,
                )
                detections.append(det)

        return detections
