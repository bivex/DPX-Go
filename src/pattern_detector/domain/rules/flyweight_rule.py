"""Go Flyweight Pattern Rule (sync.Pool & cache pools)."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType, SourceLocation


class FlyweightPatternRule(BasePatternRule):
    """Detects Flyweight Pattern in Go via sync.Pool."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.FLYWEIGHT

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for f in model.files.values():
            src = f.raw_source
            if not src:
                continue

            # Look for sync.Pool
            if "sync.Pool" in src:
                matches = re.finditer(r"([a-zA-Z0-9_]+)\s*=\s*(?:&)?sync\.Pool\s*\{", src)
                for m in matches:
                    var_name = m.group(1)
                    line = src[:m.start()].count("\n") + 1
                    loc = SourceLocation(file_path=f.file_path, line=line)

                    evidences = [
                        Evidence(
                            description=f"Flyweight memory reuse pool '{var_name}' configured with sync.Pool",
                            weight=0.80,
                            rule_code="FLYWEIGHT_SYNC_POOL",
                            location=loc,
                        )
                    ]
                    det = self._create_detection(
                        target_name=var_name,
                        target_kind="sync_pool_flyweight",
                        evidences=evidences,
                        location=loc,
                    )
                    detections.append(det)

        return detections
