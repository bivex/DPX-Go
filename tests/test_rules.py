"""Tests for DPX-Go pattern detection rules."""

from pattern_detector.adapters.outbound.parsers.native_go_parser_adapter import NativeGoParserAdapter
from pattern_detector.application.services.detection_service import DetectionService
from pattern_detector.domain.value_objects import PatternType


def test_detect_functional_options():
    code = """package server

type Option func(*Server)

func WithPort(p int) Option {
    return func(s *Server) { s.port = p }
}

func NewServer(opts ...Option) *Server {
    return &Server{}
}
"""
    parser = NativeGoParserAdapter()
    model = parser.parse_sources({"server.go": code})
    service = DetectionService()
    detections = service.detect_patterns(model)

    opt_dets = [d for d in detections if d.pattern_type == PatternType.FUNCTIONAL_OPTIONS]
    assert len(opt_dets) >= 1
    assert opt_dets[0].target_name == "Option"


def test_detect_builder_pattern():
    code = """package builder

type ConfigBuilder struct {
    host string
}

func (b *ConfigBuilder) SetHost(h string) *ConfigBuilder {
    b.host = h
    return b
}

func (b *ConfigBuilder) Build() Config {
    return Config{}
}
"""
    parser = NativeGoParserAdapter()
    model = parser.parse_sources({"builder.go": code})
    service = DetectionService()
    detections = service.detect_patterns(model)

    builder_dets = [d for d in detections if d.pattern_type == PatternType.BUILDER]
    assert len(builder_dets) >= 1
    assert builder_dets[0].target_name == "ConfigBuilder"


def test_detect_singleton_and_concurrency():
    code = """package main

import "sync"

type Registry struct {}

var (
    instance *Registry
    once sync.Once
)

func GetRegistry() *Registry {
    once.Do(func() {
        instance = &Registry{}
    })
    return instance
}

func Squarer(in <-chan int) <-chan int {
    out := make(chan int)
    return out
}
"""
    parser = NativeGoParserAdapter()
    model = parser.parse_sources({"main.go": code})
    service = DetectionService()
    detections = service.detect_patterns(model)

    singletons = [d for d in detections if d.pattern_type == PatternType.SINGLETON]
    assert len(singletons) >= 1

    pipelines = [d for d in detections if d.pattern_type == PatternType.PIPELINE]
    assert len(pipelines) >= 1


def test_detect_god_struct_and_leaks():
    code = """package smell

type HugeStruct struct {
    f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13, f14, f15 int
}

func (h *HugeStruct) M1() {}
func (h *HugeStruct) M2() {}
func (h *HugeStruct) M3() {}
func (h *HugeStruct) M4() {}
func (h *HugeStruct) M5() {}
func (h *HugeStruct) M6() {}
func (h *HugeStruct) M7() {}
func (h *HugeStruct) M8() {}
func (h *HugeStruct) M9() {}
func (h *HugeStruct) M10() {}
func (h *HugeStruct) M11() {}
func (h *HugeStruct) M12() {}
func (h *HugeStruct) M13() {}
func (h *HugeStruct) M14() {}
func (h *HugeStruct) M15() {}
func (h *HugeStruct) M16() {}

func InfiniteLeaker() {
    go func() {
        for {
        }
    }()
}
"""
    parser = NativeGoParserAdapter()
    model = parser.parse_sources({"smell.go": code})
    service = DetectionService()
    detections = service.detect_patterns(model)

    srp = [d for d in detections if d.pattern_type == PatternType.SINGLE_RESPONSIBILITY]
    assert len(srp) >= 1

    leaks = [d for d in detections if d.pattern_type == PatternType.GOROUTINE_LEAK_RISK]
    assert len(leaks) >= 1
