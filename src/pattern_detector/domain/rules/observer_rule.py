"""Go Observer / Event Emitter Pattern Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class ObserverPatternRule(BasePatternRule):
    """Detects Observer / Event Emitter Pattern in Go."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.OBSERVER

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for st in model.all_structs():
            evidences: list[Evidence] = []
            name_lower = st.name.lower()

            if "event" in name_lower or "observer" in name_lower or "emitter" in name_lower or "hub" in name_lower or "bus" in name_lower:
                evidences.append(
                    Evidence(
                        description=f"Struct '{st.name}' follows Observer / Event Bus naming convention",
                        weight=0.35,
                        rule_code="OBSERVER_NAMING",
                        location=st.location,
                    )
                )

            # Slices of channels or callback functions
            listener_fields = [
                f for f in st.fields
                if "chan " in f.type_str or "[]chan " in f.type_str or "[]func(" in f.type_str or "map[" in f.type_str and "chan" in f.type_str
                or f.name in ("listeners", "subscribers", "observers", "handlers")
            ]
            if listener_fields:
                evidences.append(
                    Evidence(
                        description=f"Maintains multi-subscriber dispatch channels/listeners '{listener_fields[0].name}: {listener_fields[0].type_str}'",
                        weight=0.60,
                        rule_code="OBSERVER_LISTENER_CHANNELS",
                        location=st.location,
                    )
                )

            # Subscribe / Publish methods
            dispatch_methods = [
                m for m_name, m in st.methods.items()
                if m_name in ("Subscribe", "Unsubscribe", "Publish", "Emit", "Notify", "AddListener", "Broadcast")
            ]
            if dispatch_methods:
                evidences.append(
                    Evidence(
                        description=f"Provides observer subscription/broadcast method(s) ({', '.join(m.name for m in dispatch_methods[:3])})",
                        weight=0.45,
                        rule_code="OBSERVER_DISPATCH_METHODS",
                        location=dispatch_methods[0].location or st.location,
                    )
                )

            if evidences:
                det = self._create_detection(
                    target_name=st.name,
                    target_kind="observer_struct",
                    evidences=evidences,
                    location=st.location,
                )
                if det.confidence.score >= 0.50:
                    detections.append(det)

        return detections
