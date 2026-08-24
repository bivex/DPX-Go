"""Detection and Report domain entities for Go Pattern Detector."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from pattern_detector.domain.value_objects import (
    Confidence,
    ConfidenceLevel,
    Evidence,
    PatternCategory,
    PatternType,
    SourceLocation,
)


@dataclass(frozen=True)
class Detection:
    """Represents an identified software design pattern or architecture smell in Go."""

    pattern_type: PatternType
    pattern_category: PatternCategory
    target_name: str
    target_kind: str  # "struct", "interface", "function", "package", "type_alias", "goroutine"
    confidence: Confidence
    primary_location: SourceLocation | None = None
    evidences: list[Evidence] = field(default_factory=list)
    related_locations: list[SourceLocation] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def level(self) -> ConfidenceLevel:
        return self.confidence.level

    @property
    def summary(self) -> str:
        if self.evidences:
            return self.evidences[0].description
        return f"{self.pattern_type.value} on {self.target_kind} '{self.target_name}'"


@dataclass
class DetectionReport:
    """Aggregated findings report of a codebase scan."""

    project_path: str
    scanned_files_count: int
    detections: list[Detection] = field(default_factory=list)
    elapsed_seconds: float = 0.0

    @property
    def total_detections_count(self) -> int:
        return len(self.detections)

    @property
    def summary_by_category(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for d in self.detections:
            cat = d.pattern_category.value
            counts[cat] = counts.get(cat, 0) + 1
        return counts

    @property
    def summary_by_confidence_level(self) -> dict[str, int]:
        counts: dict[str, int] = {level.value: 0 for level in ConfidenceLevel}
        for d in self.detections:
            counts[d.level.value] += 1
        return counts
