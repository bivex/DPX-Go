"""Go Struct Embedding (Composition) Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class StructEmbeddingRule(BasePatternRule):
    """Detects Struct Embedding composition in Go."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.STRUCT_EMBEDDING

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for st in model.all_structs():
            embedded = [f.type_str for f in st.fields if f.is_embedded] + st.embedded_types
            if embedded:
                evidences = [
                    Evidence(
                        description=f"Struct '{st.name}' implements idiomatic Go Composition Over Inheritance via anonymous embedding of ({', '.join(embedded[:3])})",
                        weight=0.75,
                        rule_code="STRUCT_EMBEDDING_COMPOSITION",
                        location=st.location,
                    )
                ]
                det = self._create_detection(
                    target_name=st.name,
                    target_kind="embedded_struct",
                    evidences=evidences,
                    location=st.location,
                )
                detections.append(det)

        return detections
