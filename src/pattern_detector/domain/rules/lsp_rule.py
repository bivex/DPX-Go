"""Go Liskov Substitution Principle (LSP) Rule (panic in interface methods)."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class LiskovSubstitutionRule(BasePatternRule):
    """Detects LSP violations in Go (methods calling panic('unimplemented'))."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.LISKOV_SUBSTITUTION

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for fn in model.all_functions():
            if fn.is_method:
                if 'panic("not implemented' in fn.body or 'panic("unimplemented' in fn.body or 'panic("TODO' in fn.body:
                    evidences = [
                        Evidence(
                            description=f"LSP Violation: Method '{fn.receiver_type}.{fn.name}' panics with unimplemented error, violating behavioral contract",
                            weight=0.85,
                            rule_code="LSP_PANIC_UNIMPLEMENTED",
                            location=fn.location,
                        )
                    ]
                    det = self._create_detection(
                        target_name=f"{fn.receiver_type}.{fn.name}",
                        target_kind="method",
                        evidences=evidences,
                        location=fn.location,
                    )
                    detections.append(det)

        return detections
