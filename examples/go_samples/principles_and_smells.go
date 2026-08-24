package smells

import (
	"context"
	"io"
)

// Fat interface violating ISP (Interface Pollution)
type MegaMonolithicRepository interface {
	GetUser(id string) (any, error)
	CreateUser(u any) error
	UpdateUser(u any) error
	DeleteUser(id string) error
	ListUsers() ([]any, error)
	GetOrder(id string) (any, error)
	CreateOrder(o any) error
	CancelOrder(id string) error
	RefundOrder(id string) error
	GenerateInvoice(id string) ([]byte, error)
}

// God Struct violating SRP
type GodManager struct {
	field1  string
	field2  string
	field3  string
	field4  string
	field5  string
	field6  string
	field7  string
	field8  string
	field9  string
	field10 string
	field11 string
	field12 string
	field13 string
}

func (g *GodManager) M1() {}
func (g *GodManager) M2() {}
func (g *GodManager) M3() {}
func (g *GodManager) M4() {}
func (g *GodManager) M5() {}
func (g *GodManager) M6() {}
func (g *GodManager) M7() {}
func (g *GodManager) M8() {}
func (g *GodManager) M9() {}
func (g *GodManager) M10() {}
func (g *GodManager) M11() {}
func (g *GodManager) M12() {}
func (g *GodManager) M13() {}
func (g *GodManager) M14() {}
func (g *GodManager) M15() {}
func (g *GodManager) M16() {}

// DIP adherence
func ProcessDataStream(ctx context.Context, r io.Reader, w io.Writer) error {
	return nil
}

// Goroutine leak risk
func LeakyBackgroundWorker() {
	go func() {
		for {
			// Infinite loop without ctx.Done() or quit channel
		}
	}()
}

// Unchecked error
func BadErrorHandler(w io.WriteCloser) {
	_ = w.Close()
}
