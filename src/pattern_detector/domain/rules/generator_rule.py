"""Go Generator Pattern Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class GeneratorPatternRule(BasePatternRule):
    """Detects Generator Pattern in Go (functions returning <-chan T with background producer goroutine)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.GENERATOR

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for fn in model.all_functions():
            # Doesn't take a channel, but returns <-chan T and spawns a goroutine
            takes_chan = any("chan " in p[1] or "<-chan" in p[1] for p in fn.params)
            returns_chan = any("<-chan" in r for r in fn.return_types)
            has_goroutine = "go func" in fn.body or "go " in fn.body

            if not takes_chan and returns_chan and has_goroutine:
                evidences = [
                    Evidence(
                        description=f"Function '{fn.name}' implements idiomatic Go Generator pattern spawning a producer goroutine and returning receive-only channel '{fn.return_type_str}'",
                        weight=0.80,
                        rule_code="GENERATOR_PRODUCER_GOROUTINE",
                        location=fn.location,
                    )
                ]
                det = self._create_detection(
                    target_name=fn.name,
                    target_kind="generator_function",
                    evidences=evidences,
                    location=fn.location,
                )
                detections.append(det)

        return detections
