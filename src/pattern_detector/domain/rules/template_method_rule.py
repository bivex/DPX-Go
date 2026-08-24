"""Go Template Method Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class TemplateMethodRule(BasePatternRule):
    """Detects Template Method in Go (base struct embedding interface and calling its methods in template workflow)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.TEMPLATE_METHOD

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for st in model.all_structs():
            # Embeds an interface
            if st.embedded_types and any(t[0].isupper() for t in st.embedded_types):
                run_methods = [
                    m for m_name, m in st.methods.items()
                    if m_name in ("Run", "Execute", "Process", "Template", "Handle")
                ]
                if run_methods:
                    evidences = [
                        Evidence(
                            description=f"Struct '{st.name}' defines Template Method workflow in '{run_methods[0].name}()' delegating specialized steps to embedded interface '{st.embedded_types[0]}'",
                            weight=0.70,
                            rule_code="TEMPLATE_METHOD_EMBEDDED_WORKFLOW",
                            location=run_methods[0].location or st.location,
                        )
                    ]
                    det = self._create_detection(
                        target_name=st.name,
                        target_kind="template_method_struct",
                        evidences=evidences,
                        location=st.location,
                    )
                    detections.append(det)

        return detections
