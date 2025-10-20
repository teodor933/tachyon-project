"""
Simple tweening system for animating float values with easing functions.

The Tween class interpolates a value over time using common easing curves, making it useful for UI animations
like button expansion, fade effects.
"""
import math


class Tween:
    """
    A float-based tweening utility with easing support.

    Example:
        t = Tween(0.0)
        t.to(1.0, duration=0.5, ease="ease_out")
        value = t.update(dt)  # call every frame
    """
    def __init__(self, initial: float = 0.0):
        """
        Initialise the tween with a starting value.
        :param initial: Starting value.
        """
        self._current = float(initial)
        self._start = float(initial)
        self._target = float(initial)
        self._elapsed = 0.0
        self._duration = 0.0
        self._ease = "linear"
        self._running = False

    @property
    def current(self) -> float:
        """Get the current interpolated value."""
        return self._current

    def to(self, target: float, duration: float, ease: str = "linear") -> None:
        """
        Start a new tween animation.

        :param target: Target value to reach.
        :param duration: Time in seconds to complete the tween.
        :param ease: Easing function name.
        """
        self._start = self._current
        self._target = float(target)
        self._duration = max(0.0001, float(duration))
        self._elapsed = 0.0
        self._ease = ease
        self._running = True

    def update(self, dt: float) -> float:
        """
        Advance the tween by delta time and return the current value.

        :param dt: Time since last update in seconds.
        :return: Current interpolated value.
        """
        if not self._running:
            return self._current
        self._elapsed += max(0.0, dt)
        t = min(1.0, self._elapsed / self._duration)
        eased = self._apply_ease(t, self._ease)
        self._current = self._start + (self._target - self._start) * eased
        if t >= 1.0:
            self._running = False
        return self._current

    def is_running(self) -> bool:
        """Check if the tween is currently active."""
        return self._running

    @staticmethod
    def _apply_ease(t: float, ease: str) -> float:
        """
        Apply an easing function to a normalised time value.

        :param t: Normalised time (0.0 to 1.0).
        :param ease: Name of easing function.
        :return: Eased time value.
        """
        if ease == "linear":
            return t
        if ease == "ease_in":
            return t * t
        if ease == "ease_out":
            return 1 - (1 - t) * (1 - t)
        if ease == "ease_in_out":
            return 0.5 * (1 - math.cos(math.pi * t))
        return t
