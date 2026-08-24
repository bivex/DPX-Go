"""Go Adapter Pattern Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class AdapterPatternRule(BasePatternRule):
    """Detects Adapter Pattern in Go (structs wrapping adaptee implementing target interface)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.ADAPTER

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for st in model.all_structs():
            evidences: list[Evidence] = []
            name_lower = st.name.lower()

            if name_lower.endswith("adapter") or "adapter" in name_lower:
                evidences.append(
                    Evidence(
                        description=f"Struct '{st.name}' follows Adapter naming convention",
                        weight=0.45,
                        rule_code="ADAPTER_NAMING",
                        location=st.location,
                    )
                )

            # Wraps an adaptee field (src, inner, adaptee, reader, writer, backend)
            inner_fields = [
                f for f in st.fields
                if f.name in ("src", "inner", "adaptee", "backend", "driver", "reader", "writer", "handler")
            ]
            if inner_fields:
                evidences.append(
                    Evidence(
                        description=f"Wraps underlying adaptee in field '{inner_fields[0].name}: {inner_fields[0].type_str}'",
                        weight=0.40,
                        rule_code="ADAPTER_WRAPS_INNER",
                        location=st.location,
                    )
                )

            # Implements standard interface methods (e.g. Read, Write, ServeHTTP, Handle)
            standard_methods = [
                m for m_name, m in st.methods.items()
                if m_name in ("Read", "Write", "ServeHTTP", "Close", "Handle", "Do")
            ]
            if standard_methods and (name_lower.endswith("adapter") or inner_fields):
                evidences.append(
                    Evidence(
                        description=f"Adapts wrapped object to standard interface by implementing '{standard_methods[0].name}()'",
                        weight=0.45,
                        rule_code="ADAPTER_TARGET_METHOD",
                        location=standard_methods[0].location or st.location,
                    )
                )

            if evidences:
                det = self._create_detection(
                    target_name=st.name,
                    target_kind="adapter_struct",
                    evidences=evidences,
                    location=st.location,
                )
                if det.confidence.score >= 0.50:
                    detections.append(det)

        return detections
