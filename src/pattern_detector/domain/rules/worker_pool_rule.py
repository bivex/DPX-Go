"""Go Worker Pool Pattern Rule."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class WorkerPoolRule(BasePatternRule):
    """Detects Worker Pool pattern in Go."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.WORKER_POOL

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        # 1. Functions spawning fixed number of workers in a loop
        for fn in model.all_functions():
            if re.search(r"for\s+[a-zA-Z0-9_]+\s*:=\s*0;\s*[a-zA-Z0-9_]+\s*<\s*(?:workers|numWorkers|num_workers|concurrency|size|wCount|[0-9]+)", fn.body) and ("go " in fn.body or "go func" in fn.body) and ("jobs" in fn.body or "tasks" in fn.body or "<-chan" in fn.body or "chan " in fn.body):
                evidences = [
                    Evidence(
                        description=f"Function '{fn.name}' implements Worker Pool pattern by spawning a fixed pool of worker goroutines over a shared jobs channel",
                        weight=0.80,
                        rule_code="WORKER_POOL_SPAWNER",
                        location=fn.location,
                    )
                ]
                det = self._create_detection(
                    target_name=fn.name,
                    target_kind="worker_pool_function",
                    evidences=evidences,
                    location=fn.location,
                )
                detections.append(det)

        # 2. Structs named WorkerPool / Pool
        for st in model.all_structs():
            if "pool" in st.name.lower() or "worker" in st.name.lower():
                job_chans = [f for f in st.fields if "chan " in f.type_str]
                if job_chans:
                    evidences = [
                        Evidence(
                            description=f"Struct '{st.name}' encapsulates bounded Worker Pool with task channel '{job_chans[0].name}: {job_chans[0].type_str}'",
                            weight=0.75,
                            rule_code="WORKER_POOL_STRUCT",
                            location=st.location,
                        )
                    ]
                    det = self._create_detection(
                        target_name=st.name,
                        target_kind="worker_pool_struct",
                        evidences=evidences,
                        location=st.location,
                    )
                    detections.append(det)

        return detections
