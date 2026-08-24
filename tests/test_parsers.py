"""Tests for DPX-Go native parser adapter."""

from pattern_detector.adapters.outbound.parsers.native_go_parser_adapter import NativeGoParserAdapter


def test_parse_go_file():
    parser = NativeGoParserAdapter()
    code = """package main

import (
    "context"
    "fmt"
)

type Option func(*Server)

type Server struct {
    port int
}

func (s *Server) Start(ctx context.Context) error {
    return nil
}
"""
    file_model = parser.parse_file("server.go", code)
    assert file_model.package == "main"
    assert "context" in file_model.imports
    assert "Server" in file_model.structs
    assert "Option" in file_model.type_aliases
    assert file_model.type_aliases["Option"].is_func_type is True
    assert "Start" in file_model.structs["Server"].methods
    assert file_model.structs["Server"].methods["Start"].is_method is True
