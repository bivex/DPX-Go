package middleware

import (
	"net/http"
	"time"
)

type Middleware func(http.Handler) http.Handler

func LoggingMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()
		next.ServeHTTP(w, r)
		_ = start
	})
}

type LoggingHandlerDecorator struct {
	next http.Handler
}

func (d *LoggingHandlerDecorator) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	d.next.ServeHTTP(w, r)
}
