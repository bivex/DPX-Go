"""Go Composite Pattern Rule (tree slices []Component)."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class CompositePatternRule(BasePatternRule):
    """Detects Composite Pattern in Go."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.COMPOSITE

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for st in model.all_structs():
            child_fields = [
                f for f in st.fields
                if f.type_str in (f"[]{st.name}", f"[]*{st.name}", "[]Component", "[]Node", "[]Element")
                or f.name in ("children", "nodes", "elements", "branches", "subItems")
            ]
            if child_fields:
                evidences = [
                    Evidence(
                        description=f"Struct '{st.name}' maintains composite child collection '{child_fields[0].name}: {child_fields[0].type_str}'",
                        weight=0.70,
                        rule_code="COMPOSITE_CHILDREN_SLICE",
                        location=st.location,
                    )
                ]
                det = self._create_detection(
                    target_name=st.name,
                    target_kind="composite_struct",
                    evidences=evidences,
                    location=st.location,
                )
                detections.append(det)

        return detections
