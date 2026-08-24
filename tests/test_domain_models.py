"""Tests for DPX-Go domain entities and value objects."""

import pytest
from pattern_detector.domain.code_model import CodeModel, FieldModel, FileModel, FunctionModel, StructModel
from pattern_detector.domain.detection import Detection, DetectionReport
from pattern_detector.domain.value_objects import (
    Confidence,
    ConfidenceLevel,
    Evidence,
    PatternCategory,
    PatternType,
    SourceLocation,
)


def test_confidence_calculation():
    ev1 = Evidence(description="Heuristic 1", weight=0.5, rule_code="H1")
    ev2 = Evidence(description="Heuristic 2", weight=0.5, rule_code="H2")

    # 1 - (1 - 0.5) * (1 - 0.5) = 1 - 0.25 = 0.75
    conf = Confidence.from_evidences([ev1, ev2])
    assert conf.score == 0.75
    assert conf.level == ConfidenceLevel.HIGH
    assert conf.percentage_str == "75%"


def test_source_location_str():
    loc = SourceLocation(file_path="pkg/server/server.go", line=42, column=5)
    assert str(loc) == "pkg/server/server.go:42:5"


def test_circular_dependency_detection():
    model = CodeModel()
    f1 = FileModel(package="pkg_a", file_path="a.go", imports=['"github.com/org/repo/pkg_b"'])
    f2 = FileModel(package="pkg_b", file_path="b.go", imports=['"github.com/org/repo/pkg_a"'])
    model.files["a.go"] = f1
    model.files["b.go"] = f2

    cycles = model.find_circular_dependencies()
    assert len(cycles) >= 1
    assert "pkg_a" in cycles[0]
    assert "pkg_b" in cycles[0]
