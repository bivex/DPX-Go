"""Go Builder Pattern Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class BuilderPatternRule(BasePatternRule):
    """Detects Builder Pattern in Go."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.BUILDER

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for st in model.all_structs():
            evidences: list[Evidence] = []
            name_lower = st.name.lower()

            if name_lower.endswith("builder") or "builder" in name_lower:
                evidences.append(
                    Evidence(
                        description=f"Struct '{st.name}' follows Builder naming convention",
                        weight=0.40,
                        rule_code="BUILDER_NAMING",
                        location=st.location,
                    )
                )

            # Terminal Build / Create method
            build_methods = [
                m for m_name, m in st.methods.items()
                if m_name in ("Build", "Create", "Compile", "Finish", "Generate")
            ]
            if build_methods:
                evidences.append(
                    Evidence(
                        description=f"Provides terminal construction method '{build_methods[0].name}()' returning built instance",
                        weight=0.45,
                        rule_code="BUILDER_TERMINAL_METHOD",
                        location=build_methods[0].location or st.location,
                    )
                )

            # Fluent chaining methods returning *Struct
            chaining_methods = [
                m for m_name, m in st.methods.items()
                if (f"*{st.name}" in m.return_type_str or st.name in m.return_type_str)
                and m_name not in ("Build", "Create", "New")
            ]
            if len(chaining_methods) >= 4:
                evidences.append(
                    Evidence(
                        description=f"Implements Fluent Builder chaining API with {len(chaining_methods)} method(s) returning *{st.name} ({', '.join(m.name for m in chaining_methods[:4])})",
                        weight=0.65,
                        rule_code="BUILDER_FLUENT_SETTERS",
                        location=chaining_methods[0].location or st.location,
                    )
                )
            elif len(chaining_methods) >= 2:
                evidences.append(
                    Evidence(
                        description=f"Contains {len(chaining_methods)} fluent chaining configuration method(s) returning *{st.name} ({', '.join(m.name for m in chaining_methods[:3])})",
                        weight=0.45,
                        rule_code="BUILDER_FLUENT_SETTERS",
                        location=chaining_methods[0].location or st.location,
                    )
                )

            if evidences:
                det = self._create_detection(
                    target_name=st.name,
                    target_kind="builder_struct",
                    evidences=evidences,
                    location=st.location,
                )
                if det.confidence.score >= 0.50:
                    detections.append(det)

        return detections
