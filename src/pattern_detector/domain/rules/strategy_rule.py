"""Go Strategy Pattern Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class StrategyPatternRule(BasePatternRule):
    """Detects Strategy Pattern in Go (strategy interfaces or func types)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.STRATEGY

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        # 1. Strategy Interfaces
        for iface in model.all_interfaces():
            name_lower = iface.name.lower()
            if name_lower.endswith("strategy") or "policy" in name_lower or "algorithm" in name_lower:
                evidences = [
                    Evidence(
                        description=f"Interface '{iface.name}' defines polymorphic Strategy algorithm interface",
                        weight=0.75,
                        rule_code="STRATEGY_INTERFACE_NAMING",
                        location=iface.location,
                    )
                ]
                det = self._create_detection(
                    target_name=iface.name,
                    target_kind="strategy_interface",
                    evidences=evidences,
                    location=iface.location,
                )
                detections.append(det)

        # 2. Strategy Function Types
        for alias in model.all_type_aliases():
            if alias.is_func_type and ("Strategy" in alias.name or "Policy" in alias.name or "Matcher" in alias.name or "Filter" in alias.name):
                evidences = [
                    Evidence(
                        description=f"Function type '{alias.name}' ({alias.underlying_type}) acts as first-class strategy callback",
                        weight=0.70,
                        rule_code="STRATEGY_FUNC_TYPE",
                        location=alias.location,
                    )
                ]
                det = self._create_detection(
                    target_name=alias.name,
                    target_kind="strategy_func_type",
                    evidences=evidences,
                    location=alias.location,
                )
                detections.append(det)

        return detections
