"""Go Open/Closed Principle (OCP) Rule (Type Switch Cascades)."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class OpenClosedPrincipleRule(BasePatternRule):
    """Detects OCP violations in Go (large type switch cascades switch .(type))."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.OPEN_CLOSED

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for fn in model.all_functions():
            if "switch" in fn.body and ".(type)" in fn.body:
                cases = len(re.findall(r"\bcase\s+", fn.body))
                if cases >= 5:
                    evidences = [
                        Evidence(
                            description=f"OCP Violation: Function '{fn.name}' uses type switch with {cases} branches; consider interface method polymorphism for open extensibility",
                            weight=0.75,
                            rule_code="OCP_TYPE_SWITCH_CASCADE",
                            location=fn.location,
                        )
                    ]
                    det = self._create_detection(
                        target_name=fn.name,
                        target_kind="function",
                        evidences=evidences,
                        location=fn.location,
                    )
                    detections.append(det)

        return detections
