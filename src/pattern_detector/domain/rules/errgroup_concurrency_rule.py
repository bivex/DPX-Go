"""Go ErrGroup Concurrency Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class ErrgroupConcurrencyRule(BasePatternRule):
    """Detects errgroup.Group concurrency coordination in Go."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.ERRGROUP_CONCURRENCY

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for fn in model.all_functions():
            if "errgroup.WithContext" in fn.body or "errgroup.Group" in fn.body or ".Go(func()" in fn.body:
                evidences = [
                    Evidence(
                        description=f"Function '{fn.name}' coordinates concurrent subtasks with errgroup.Group for automatic cancellation and error collection",
                        weight=0.85,
                        rule_code="ERRGROUP_CONCURRENCY",
                        location=fn.location,
                    )
                ]
                det = self._create_detection(
                    target_name=fn.name,
                    target_kind="errgroup_coordinator",
                    evidences=evidences,
                    location=fn.location,
                )
                detections.append(det)

        return detections
