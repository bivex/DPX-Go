"""Go Goroutine Leak Risk Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class GoroutineLeakRule(BasePatternRule):
    """Detects Goroutine Leak Risk in Go (goroutines looping or blocking on channels without ctx.Done())."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.GOROUTINE_LEAK_RISK

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for fn in model.all_functions():
            if ("go func" in fn.body or "go " in fn.body) and ("for {" in fn.body or "for select" in fn.body or "for {" in fn.body):
                if "ctx.Done()" not in fn.body and "context" not in fn.body and "quit" not in fn.body and "close(" not in fn.body:
                    evidences = [
                        Evidence(
                            description=f"Safety Audit (Goroutine Leak Risk): Function '{fn.name}' spawns an infinite goroutine loop without listening for 'ctx.Done()' cancellation or a quit channel",
                            weight=0.80,
                            rule_code="GOROUTINE_LEAK_RISK",
                            location=fn.location,
                        )
                    ]
                    det = self._create_detection(
                        target_name=fn.name,
                        target_kind="goroutine_leak",
                        evidences=evidences,
                        location=fn.location,
                    )
                    detections.append(det)

        return detections
