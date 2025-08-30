class GameStateManager:
    def __init__(self, game):
        self.game = game
        self.current_state = None

    def change_state(self, new_state):
        self.current_state = new_state

    def handle_events(self, events):
        if self.current_state:
            self.current_state.handle_events(events)

    def update(self, dt):
        if self.current_state:
            self.current_state.update(dt)

    def render(self, screen):
        if self.current_state:
            self.current_state.render(screen)
