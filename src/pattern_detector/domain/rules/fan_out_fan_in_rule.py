"""Go Fan-Out / Fan-In Concurrency Pattern Rule."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class FanOutFanInRule(BasePatternRule):
    """Detects Fan-Out / Fan-In pattern in Go."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.FAN_OUT_FAN_IN

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for fn in model.all_functions():
            # Merges variadic channels or multiple input channels via sync.WaitGroup
            variadic_chan = any("...<-chan" in p[1] or "...chan " in p[1] for p in fn.params)
            has_wg = "sync.WaitGroup" in fn.body or "wg.Add" in fn.body or "wg.Wait" in fn.body
            returns_chan = any("<-chan" in r or "chan " in r for r in fn.return_types)

            if (variadic_chan or "merge" in fn.name.lower()) and has_wg and returns_chan:
                evidences = [
                    Evidence(
                        description=f"Function '{fn.name}' implements Fan-In channel multiplexer using sync.WaitGroup to merge multiple concurrent streams into single output channel",
                        weight=0.85,
                        rule_code="FAN_IN_CHANNEL_MERGE",
                        location=fn.location,
                    )
                ]
                det = self._create_detection(
                    target_name=fn.name,
                    target_kind="fan_in_function",
                    evidences=evidences,
                    location=fn.location,
                )
                detections.append(det)

        return detections
