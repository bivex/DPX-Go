"""Go Memento Pattern Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class MementoPatternRule(BasePatternRule):
    """Detects Memento Pattern in Go (SaveSnapshot / Restore)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.MEMENTO

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for st in model.all_structs():
            save_methods = [
                m for m_name, m in st.methods.items()
                if m_name in ("SaveSnapshot", "Snapshot", "CreateMemento", "SaveState")
            ]
            restore_methods = [
                m for m_name, m in st.methods.items()
                if m_name in ("Restore", "RestoreSnapshot", "SetMemento", "LoadState")
            ]

            if save_methods and restore_methods:
                evidences = [
                    Evidence(
                        description=f"Struct '{st.name}' provides Memento state snapshot creation '{save_methods[0].name}()' and restoration '{restore_methods[0].name}()'",
                        weight=0.80,
                        rule_code="MEMENTO_SAVE_RESTORE",
                        location=save_methods[0].location or st.location,
                    )
                ]
                det = self._create_detection(
                    target_name=st.name,
                    target_kind="memento_originator",
                    evidences=evidences,
                    location=st.location,
                )
                detections.append(det)

        return detections
