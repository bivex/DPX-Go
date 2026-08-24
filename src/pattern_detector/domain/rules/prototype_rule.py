"""Go Prototype Pattern Rule (Clone methods)."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class PrototypePatternRule(BasePatternRule):
    """Detects Prototype pattern in Go via Clone() methods."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.PROTOTYPE

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for st in model.all_structs():
            clone_methods = [m for m_name, m in st.methods.items() if m_name in ("Clone", "DeepCopy")]
            if clone_methods:
                cm = clone_methods[0]
                evidences = [
                    Evidence(
                        description=f"Struct '{st.name}' implements Prototype pattern via '{cm.name}()' method returning cloned instance",
                        weight=0.75,
                        rule_code="PROTOTYPE_CLONE_METHOD",
                        location=cm.location or st.location,
                    )
                ]
                det = self._create_detection(
                    target_name=st.name,
                    target_kind="prototype_struct",
                    evidences=evidences,
                    location=st.location,
                )
                detections.append(det)

        return detections
