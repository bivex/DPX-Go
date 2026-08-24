"""Go Dependency Inversion Principle (DIP) Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class DependencyInversionRule(BasePatternRule):
    """Detects DIP in Go (functions accepting interface abstractions)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.DEPENDENCY_INVERSION

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for fn in model.all_functions():
            iface_params = [
                (p_name, p_type) for p_name, p_type in fn.params
                if p_type in ("io.Reader", "io.Writer", "io.ReadCloser", "http.Handler", "driver.Driver", "context.Context")
                or (p_type[0].isupper() and not p_type.startswith("*") and p_type not in ("string", "int", "bool", "time.Time"))
            ]
            if len(iface_params) >= 2:
                evidences = [
                    Evidence(
                        description=f"DIP Adherence: Function '{fn.name}' depends on interface abstraction(s) ({', '.join(f'{p[0]} {p[1]}' for p in iface_params[:2])}) rather than concrete struct pointers",
                        weight=0.75,
                        rule_code="DIP_INTERFACE_PARAMETER",
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
