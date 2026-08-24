"""Go Abstract Factory Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class AbstractFactoryRule(BasePatternRule):
    """Detects Abstract Factory interfaces producing families of products in Go."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.ABSTRACT_FACTORY

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for iface in model.all_interfaces():
            evidences: list[Evidence] = []
            name_lower = iface.name.lower()

            if name_lower.endswith("factory") or "abstractfactory" in name_lower:
                evidences.append(
                    Evidence(
                        description=f"Interface '{iface.name}' follows Abstract Factory naming convention",
                        weight=0.45,
                        rule_code="ABSTRACT_FACTORY_NAMING",
                        location=iface.location,
                    )
                )

            # Factory methods in interface returning interface/pointer types
            factory_methods = [
                m for m in iface.methods.values()
                if (m.name.startswith("Create") or m.name.startswith("Build") or m.name.startswith("New"))
                and m.return_types
            ]
            if len(factory_methods) >= 2:
                evidences.append(
                    Evidence(
                        description=f"Declares family of {len(factory_methods)} product creation method(s) ({', '.join(m.name for m in factory_methods[:3])})",
                        weight=0.55,
                        rule_code="ABSTRACT_FACTORY_METHODS",
                        location=iface.location,
                    )
                )

            if evidences:
                det = self._create_detection(
                    target_name=iface.name,
                    target_kind="abstract_factory_interface",
                    evidences=evidences,
                    location=iface.location,
                )
                if det.confidence.score >= 0.50:
                    detections.append(det)

        return detections
