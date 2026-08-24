"""Go Context Propagation Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class ContextPropagationRule(BasePatternRule):
    """Detects idiomatic context.Context propagation in Go."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.CONTEXT_PROPAGATION

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for fn in model.all_functions():
            if fn.params and fn.params[0][1] in ("context.Context", "ctx.Context"):
                evidences = [
                    Evidence(
                        description=f"Function '{fn.name}' adheres to idiomatic Go context propagation passing '{fn.params[0][0]}: {fn.params[0][1]}' as first parameter",
                        weight=0.70,
                        rule_code="CONTEXT_FIRST_PARAM",
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
