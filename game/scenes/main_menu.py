import pygame

from engine.core.game_state_manager import GameStateManager
from engine.core.scene import Scene
from game.scenes.game_level import GameLevel

class MainMenuScene(Scene):
    def on_enter(self):
        # to create UI entities here with sprites for buttons later
        self.font = pygame.font.Font(None, 48)
        self.title_text = self.font.render("Tachyon Engine", True, (255, 255, 255))
        self.start_text = self.font.render("Press N for New Game", True, (200, 200, 200))
        self.controls_text = self.font.render("Use WASD to Move, Space to Jump", True, (150, 150, 150))

        self.state_manager = GameStateManager(self.world)
        if self.state_manager.has_save_file():
            self.continue_text = self.font.render("Press C to Continue", True, (200, 200, 200))
        else:
            self.continue_text = None

    def update(self, dt):
        # handle input before calling parent update
        keys = pygame.key.get_pressed()
        if keys[pygame.K_n]:
            self.engine.change_scene(lambda ge: GameLevel(ge, "data/levels/level_1.json", load_save=False))
        elif keys[pygame.K_c] and self.continue_text:
            self.engine.change_scene(lambda ge: GameLevel(ge, "data/levels/level_1.json", load_save=True))

        # let systems update
        super().update(dt)

        screen = self.engine.screen
        screen.fill((50, 50, 100))

        # centre text
        screen.blit(self.title_text,
                    (screen.get_width() // 2 - self.title_text.get_width() // 2, 200))
        screen.blit(self.start_text,
                    (screen.get_width() // 2 - self.start_text.get_width() // 2, 300))
        screen.blit(self.controls_text,
                    (screen.get_width() // 2 - self.controls_text.get_width() // 2, 400))

        if self.continue_text:
            screen.blit(self.continue_text, (screen.get_width() // 2 - self.continue_text.get_width() // 2, 350))
