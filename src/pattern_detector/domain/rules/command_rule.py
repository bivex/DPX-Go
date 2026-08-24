"""Go Command Pattern Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class CommandPatternRule(BasePatternRule):
    """Detects Command Pattern in Go."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.COMMAND

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        # 1. Command Interfaces
        for iface in model.all_interfaces():
            exec_methods = [m for m_name, m in iface.methods.items() if m_name in ("Execute", "Do", "Undo", "Run")]
            if exec_methods and ("Command" in iface.name or "Action" in iface.name or "Job" in iface.name or "Task" in iface.name):
                evidences = [
                    Evidence(
                        description=f"Interface '{iface.name}' defines executable Command abstraction via '{exec_methods[0].name}()'",
                        weight=0.75,
                        rule_code="COMMAND_INTERFACE",
                        location=iface.location,
                    )
                ]
                det = self._create_detection(
                    target_name=iface.name,
                    target_kind="command_interface",
                    evidences=evidences,
                    location=iface.location,
                )
                detections.append(det)

        # 2. Command Structs
        for st in model.all_structs():
            exec_methods = [m for m_name, m in st.methods.items() if m_name in ("Execute", "Undo")]
            if exec_methods and st.name.lower().endswith("command"):
                evidences = [
                    Evidence(
                        description=f"Struct '{st.name}' encapsulates executable command operation with '{exec_methods[0].name}()'",
                        weight=0.70,
                        rule_code="COMMAND_STRUCT",
                        location=st.location,
                    )
                ]
                det = self._create_detection(
                    target_name=st.name,
                    target_kind="command_struct",
                    evidences=evidences,
                    location=st.location,
                )
                detections.append(det)

        return detections
