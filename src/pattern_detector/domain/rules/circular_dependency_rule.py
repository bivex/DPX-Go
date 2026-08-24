"""Go Circular Package Dependency Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class CircularDependencyRule(BasePatternRule):
    """Detects circular import cycles between Go packages."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.CIRCULAR_DEPENDENCY

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        cycles = model.find_circular_dependencies()

        for cycle in cycles:
            cycle_str = " ➔ ".join(cycle) + " ➔ " + cycle[0]
            first_pkg = cycle[0]
            loc = None
            for f in model.files.values():
                if f.package == first_pkg:
                    loc = f.location
                    break

            evidences = [
                Evidence(
                    description=f"Circular package import cycle detected: {cycle_str}",
                    weight=0.85,
                    rule_code="CIRCULAR_PACKAGE_IMPORT_CYCLE",
                    location=loc,
                )
            ]

            det = self._create_detection(
                target_name=" ⇄ ".join(cycle),
                target_kind="package_cycle",
                evidences=evidences,
                location=loc,
            )
            detections.append(det)

        return detections
