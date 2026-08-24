package events

type Event struct {
	Topic   string
	Payload []byte
}

type EventHub struct {
	listeners map[string][]chan Event
}

func NewEventHub() *EventHub {
	return &EventHub{
		listeners: make(map[string][]chan Event),
	}
}

func (h *EventHub) Subscribe(topic string) <-chan Event {
	ch := make(chan Event, 10)
	h.listeners[topic] = append(h.listeners[topic], ch)
	return ch
}

func (h *EventHub) Publish(e Event) {
	for _, ch := range h.listeners[e.Topic] {
		ch <- e
	}
}
