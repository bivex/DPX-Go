"""Go Visitor Pattern Rule (AST Visitor, Walk/Visit)."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class VisitorPatternRule(BasePatternRule):
    """Detects Visitor Pattern in Go."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.VISITOR

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for iface in model.all_interfaces():
            visit_methods = [m for m_name, m in iface.methods.items() if m_name.startswith("Visit")]
            if visit_methods or iface.name.lower().endswith("visitor"):
                evidences = [
                    Evidence(
                        description=f"Interface '{iface.name}' defines AST Visitor traversal protocol with visit method(s) ({', '.join(m.name for m in visit_methods[:3])})",
                        weight=0.75,
                        rule_code="VISITOR_INTERFACE",
                        location=iface.location,
                    )
                ]
                det = self._create_detection(
                    target_name=iface.name,
                    target_kind="visitor_interface",
                    evidences=evidences,
                    location=iface.location,
                )
                detections.append(det)

        return detections
