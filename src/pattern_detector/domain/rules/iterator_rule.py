"""Go Iterator Pattern Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class IteratorPatternRule(BasePatternRule):
    """Detects Iterator Pattern in Go (Next()/HasNext(), iter.Seq, or Channel Iterators)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.ITERATOR

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        # 1. Iterator Interfaces
        for iface in model.all_interfaces():
            next_methods = [m for m_name, m in iface.methods.items() if m_name in ("Next", "HasNext", "Iter")]
            if len(next_methods) >= 1 and ("Iterator" in iface.name or "Cursor" in iface.name or "Scanner" in iface.name):
                evidences = [
                    Evidence(
                        description=f"Interface '{iface.name}' defines Iterator collection traversal interface via '{next_methods[0].name}()'",
                        weight=0.80,
                        rule_code="ITERATOR_INTERFACE",
                        location=iface.location,
                    )
                ]
                det = self._create_detection(
                    target_name=iface.name,
                    target_kind="iterator_interface",
                    evidences=evidences,
                    location=iface.location,
                )
                detections.append(det)

        # 2. Struct Iterators
        for st in model.all_structs():
            next_methods = [m for m_name, m in st.methods.items() if m_name in ("Next", "HasNext")]
            if next_methods and (st.name.lower().endswith("iterator") or st.name.lower().endswith("cursor") or st.name.lower().endswith("scanner")):
                evidences = [
                    Evidence(
                        description=f"Struct '{st.name}' implements Iterator state traversal via '{next_methods[0].name}()'",
                        weight=0.75,
                        rule_code="ITERATOR_STRUCT",
                        location=st.location,
                    )
                ]
                det = self._create_detection(
                    target_name=st.name,
                    target_kind="iterator_struct",
                    evidences=evidences,
                    location=st.location,
                )
                detections.append(det)

        return detections
