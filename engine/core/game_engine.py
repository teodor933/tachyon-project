import pygame


class GameEngine:
    """Main game engine class"""
    def __init__(self, width=1280, height=720, title="Tachyon Engine", fps=60):
        pygame.init()

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)

        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = fps

        self.current_scene = None
        self.next_scene = None

    def change_scene(self, scene):
        """Change to a new scene"""
        self.next_scene = scene(self) # takes in game engine

    def run(self):
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(self.fps) / 1000.0 # delta time in seconds

            # handle scene transitions
            if self.next_scene:
                if self.current_scene:
                    self.current_scene.on_exit()
                self.current_scene = self.next_scene
                self.current_scene.on_enter()
                self.next_scene = None

            # handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # update current scene
            if self.current_scene:
                self.current_scene.update(dt)

            # update display
            pygame.display.flip()

        pygame.quit()