"""Go Interface Pollution / Fat Interface Rule (ISP Violation)."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class InterfacePollutionRule(BasePatternRule):
    """Detects Interface Pollution in Go (Fat interfaces with ≥8 methods)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.INTERFACE_POLLUTION

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for iface in model.all_interfaces():
            method_count = len(iface.methods)
            if method_count >= 8:
                evidences = [
                    Evidence(
                        description=f"Interface Pollution (ISP Violation): Interface '{iface.name}' declares {method_count} methods; idiomatic Go encourages small, single-purpose interfaces (1-2 methods)",
                        weight=0.80,
                        rule_code="INTERFACE_POLLUTION_FAT_INTERFACE",
                        location=iface.location,
                    )
                ]
                det = self._create_detection(
                    target_name=iface.name,
                    target_kind="fat_interface",
                    evidences=evidences,
                    location=iface.location,
                )
                detections.append(det)

        return detections
