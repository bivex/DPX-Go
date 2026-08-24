"""Go Chain of Responsibility Rule (Onion Middleware func(http.Handler) http.Handler)."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class ChainOfResponsibilityRule(BasePatternRule):
    """Detects Chain of Responsibility / Onion Middleware in Go."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.CHAIN_OF_RESPONSIBILITY

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        # 1. Functional Middleware: func(http.Handler) http.Handler
        for alias in model.all_type_aliases():
            if alias.is_func_type and "Handler" in alias.underlying_type and "func(" in alias.underlying_type:
                evidences = [
                    Evidence(
                        description=f"Type '{alias.name}' ({alias.underlying_type}) implements Chain of Responsibility middleware pipeline wrapper",
                        weight=0.75,
                        rule_code="CHAIN_OF_RESPONSIBILITY_MIDDLEWARE_TYPE",
                        location=alias.location,
                    )
                ]
                det = self._create_detection(
                    target_name=alias.name,
                    target_kind="middleware_type",
                    evidences=evidences,
                    location=alias.location,
                )
                detections.append(det)

        # 2. Struct Handlers holding next handler
        for st in model.all_structs():
            next_fields = [f for f in st.fields if f.name in ("next", "nextHandler", "successor")]
            if next_fields and (st.name.lower().endswith("handler") or st.name.lower().endswith("middleware")):
                evidences = [
                    Evidence(
                        description=f"Struct '{st.name}' maintains forward successor chain '{next_fields[0].name}: {next_fields[0].type_str}'",
                        weight=0.70,
                        rule_code="CHAIN_OF_RESPONSIBILITY_NEXT_FIELD",
                        location=st.location,
                    )
                ]
                det = self._create_detection(
                    target_name=st.name,
                    target_kind="chain_handler_struct",
                    evidences=evidences,
                    location=st.location,
                )
                detections.append(det)

        return detections
