"""Go State Pattern Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class StatePatternRule(BasePatternRule):
    """Detects State Pattern in Go."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.STATE

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for iface in model.all_interfaces():
            if iface.name.lower().endswith("state") or iface.name.lower().endswith("status"):
                evidences = [
                    Evidence(
                        description=f"Interface '{iface.name}' defines polymorphic State interface with {len(iface.methods)} transition/handling action(s)",
                        weight=0.75,
                        rule_code="STATE_INTERFACE",
                        location=iface.location,
                    )
                ]
                det = self._create_detection(
                    target_name=iface.name,
                    target_kind="state_interface",
                    evidences=evidences,
                    location=iface.location,
                )
                detections.append(det)

        return detections
