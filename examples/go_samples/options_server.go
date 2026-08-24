package server

import (
	"context"
	"time"
)

type Server struct {
	addr    string
	port    int
	timeout time.Duration
	tls     bool
}

type Option func(*Server)

func WithPort(port int) Option {
	return func(s *Server) {
		s.port = port
	}
}

func WithTimeout(t time.Duration) Option {
	return func(s *Server) {
		s.timeout = t
	}
}

func WithTLS(enabled bool) Option {
	return func(s *Server) {
		s.tls = enabled
	}
}

func NewServer(addr string, opts ...Option) *Server {
	srv := &Server{
		addr:    addr,
		port:    8080,
		timeout: 30 * time.Second,
	}
	for _, opt := range opts {
		opt(srv)
	}
	return srv
}

func (s *Server) Start(ctx context.Context) error {
	return nil
}
