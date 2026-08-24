"""Go Singleton Pattern Rule (sync.Once / once.Do)."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType, SourceLocation


class SingletonPatternRule(BasePatternRule):
    """Detects Singleton pattern in Go via sync.Once."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.SINGLETON

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for f in model.files.values():
            src = f.raw_source
            if not src:
                continue

            # Look for sync.Once and once.Do
            if "sync.Once" in src and ".Do(" in src:
                matches = re.finditer(r"func\s+(?:Get|Instance|New|Shared)([a-zA-Z0-9_]*)\s*\(", src)
                for m in matches:
                    fn_name = m.group(0).replace("func", "").split("(")[0].strip()
                    line = src[:m.start()].count("\n") + 1
                    loc = SourceLocation(file_path=f.file_path, line=line)

                    evidences = [
                        Evidence(
                            description=f"Thread-safe Singleton accessor '{fn_name}()' lazily initializes global instance via sync.Once (once.Do)",
                            weight=0.85,
                            rule_code="SINGLETON_SYNC_ONCE",
                            location=loc,
                        )
                    ]
                    det = self._create_detection(
                        target_name=fn_name,
                        target_kind="singleton_accessor",
                        evidences=evidences,
                        location=loc,
                    )
                    detections.append(det)

        return detections
