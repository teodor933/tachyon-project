from collections import defaultdict


class EventBus:
    def __init__(self):
        self._listeners = defaultdict(list)

    def subscribe(self, event_type, listener):
        """Subscribe a listener function to an event type."""
        if listener not in self._listeners[event_type]:
            self._listeners[event_type].append(listener)

    def unsubscribe(self, event_type, listener):
        """Unsubscribe a listener from an event type."""
        if event_type in self._listeners:
            try:
                self._listeners[event_type].remove(listener)
            except ValueError:
                pass

    def emit(self, event_type, *args, **kwargs):
        """Emit an event, calling all subscribed listeners."""
        for listener in self._listeners.get(event_type, []):
            listener(*args, **kwargs)