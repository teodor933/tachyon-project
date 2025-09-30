import pygame
from engine.core.scene import Scene
from engine.systems.render_system import RenderSystem
from game.scenes.test_level import TestLevel

class MainMenuScene(Scene):
    def on_enter(self):
        # adding render system for now
        self.render_system = self.add_system(RenderSystem(self.engine.screen))

        # to create UI entities here with sprites for buttons later
        self.font = pygame.font.Font(None, 48)
        self.title_text = self.font.render("Tachyon Engine", True, (255, 255, 255))
        self.start_text = self.font.render("Press SPACE to Start", True, (200, 200, 200))
        self.controls_text = self.font.render("Use WASD to Move, Space to Jump", True, (150, 150, 150))

    def update(self, dt):
        # handle input before calling parent update
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.engine.change_scene(TestLevel)

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
