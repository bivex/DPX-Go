"""Go Interpreter Pattern Rule (Eval method over AST interfaces)."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class InterpreterPatternRule(BasePatternRule):
    """Detects Interpreter Pattern in Go."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.INTERPRETER

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for iface in model.all_interfaces():
            eval_methods = [m for m_name, m in iface.methods.items() if m_name in ("Eval", "Evaluate", "Interpret")]
            if eval_methods and ("Expr" in iface.name or "Node" in iface.name or "Expression" in iface.name or "AST" in iface.name):
                evidences = [
                    Evidence(
                        description=f"Interface '{iface.name}' defines AST Interpreter expression evaluation protocol '{eval_methods[0].name}()'",
                        weight=0.75,
                        rule_code="INTERPRETER_INTERFACE",
                        location=iface.location,
                    )
                ]
                det = self._create_detection(
                    target_name=iface.name,
                    target_kind="interpreter_interface",
                    evidences=evidences,
                    location=iface.location,
                )
                detections.append(det)

        return detections
