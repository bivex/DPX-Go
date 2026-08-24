"""Go Channel Pipeline Pattern Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class PipelinePatternRule(BasePatternRule):
    """Detects Go Channel Pipeline Pattern (stages taking and returning channels)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.PIPELINE

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for fn in model.all_functions():
            # Pipeline stage takes an in channel and returns an out channel
            takes_chan = any("chan " in p[1] or "<-chan" in p[1] for p in fn.params)
            returns_chan = any("<-chan" in r or "chan " in r for r in fn.return_types)

            if takes_chan and returns_chan:
                evidences = [
                    Evidence(
                        description=f"Function '{fn.name}' implements idiomatic Go Pipeline stage streaming data from input channel into output channel",
                        weight=0.85,
                        rule_code="PIPELINE_CHANNEL_STAGE",
                        location=fn.location,
                    )
                ]
                det = self._create_detection(
                    target_name=fn.name,
                    target_kind="pipeline_stage_function",
                    evidences=evidences,
                    location=fn.location,
                )
                detections.append(det)

        return detections
