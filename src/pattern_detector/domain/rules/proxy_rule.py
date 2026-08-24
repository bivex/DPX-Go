"""Go Proxy Pattern Rule (surrogate caching/RPC wrappers)."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class ProxyPatternRule(BasePatternRule):
    """Detects Proxy Pattern in Go."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.PROXY

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for st in model.all_structs():
            evidences: list[Evidence] = []
            name_lower = st.name.lower()

            if "proxy" in name_lower or "lazy" in name_lower or "cached" in name_lower:
                evidences.append(
                    Evidence(
                        description=f"Struct '{st.name}' follows Proxy naming convention",
                        weight=0.45,
                        rule_code="PROXY_NAMING",
                        location=st.location,
                    )
                )

            real_fields = [f for f in st.fields if f.name in ("real", "target", "client", "upstream", "backend")]
            if real_fields:
                evidences.append(
                    Evidence(
                        description=f"Holds reference to target subject '{real_fields[0].name}: {real_fields[0].type_str}' to control access",
                        weight=0.45,
                        rule_code="PROXY_HOLDS_SUBJECT",
                        location=st.location,
                    )
                )

            if evidences:
                det = self._create_detection(
                    target_name=st.name,
                    target_kind="proxy_struct",
                    evidences=evidences,
                    location=st.location,
                )
                if det.confidence.score >= 0.50:
                    detections.append(det)

        return detections
