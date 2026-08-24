"""Go Unchecked Error Rule (_ = fn())."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class UncheckedErrorRule(BasePatternRule):
    """Detects unchecked errors in Go (e.g. _ = fn())."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.UNCHECKED_ERROR

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for fn in model.all_functions():
            ignored_errors = re.findall(r"_\s*,\s*_\s*=\s*[a-zA-Z0-9_]+\.|_\s*=\s*[a-zA-Z0-9_]+\.(?:Close|Write|Read|Flush)\(", fn.body)
            if ignored_errors:
                evidences = [
                    Evidence(
                        description=f"Safety Audit (Unchecked Error): Function '{fn.name}' explicitly ignores returned error(s) ({ignored_errors[0][:30]}...); always check err != nil",
                        weight=0.75,
                        rule_code="UNCHECKED_ERROR_RETURN",
                        location=fn.location,
                    )
                ]
                det = self._create_detection(
                    target_name=fn.name,
                    target_kind="unchecked_error",
                    evidences=evidences,
                    location=fn.location,
                )
                detections.append(det)

        return detections
