class GameStateManager:
    def __init__(self, game):
        self.game = game
        self.stack = []

    def push(self, state):
        self.stack.append(state)

    def pop(self):
        if self.stack:
            self.stack[-1].on_exit()
            self.stack.pop()

    def change(self, new_state):
        while self.stack:
            self.pop()
        self.push(new_state)

    def handle_events(self, events):
        if self.stack:
            self.stack[-1].handle_events(events)

    def update(self, dt):
        if self.stack:
            self.stack[-1].update(dt)

    def render(self, screen):
        for state in self.stack:
            state.render(screen)
