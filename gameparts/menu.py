import pygame
import sys
import os

class Menu:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Spellcaster Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 72)
        self.small_font = pygame.font.Font(None, 36)
        self.background = pygame.image.load("visuals/background.jpg").convert()
        self.main_menu_background = pygame.image.load("visuals/mainmenu.png").convert()
        self.main_menu_background = pygame.transform.scale(self.main_menu_background, (800, 600))  # Resize to fit the screen
        self.selected_characters = [None, None]
        self.wizzL_images = [pygame.transform.scale(pygame.image.load(os.path.join("visuals/wizzL", img)).convert_alpha(), (150, 150)) for img in os.listdir("visuals/wizzL")]
        self.wizzR_images = [pygame.transform.scale(pygame.image.load(os.path.join("visuals/wizzR", img)).convert_alpha(), (150, 150)) for img in os.listdir("visuals/wizzR")]
        self.wizzL_index = 0
        self.wizzR_index = 0
        self.arrow_left = pygame.transform.scale(pygame.image.load("visuals/arrow_left.png").convert_alpha(), (70, 70))
        self.arrow_right = pygame.transform.scale(pygame.image.load("visuals/arrow_right.png").convert_alpha(), (70, 70))
        self.confirm_button = pygame.transform.scale(pygame.image.load("visuals/confirm_button.png").convert_alpha(), (100, 90))
        self.play_button = pygame.transform.scale(pygame.image.load("visuals/play_button.png").convert_alpha(), (200, 180))
        self.start_button = pygame.transform.scale(pygame.image.load("visuals/play_button.png").convert_alpha(), (200, 180))
        self.voice_line = pygame.mixer.Sound("sounds/characterselect.wav")

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def main_menu(self):
        while True:
            self.screen.blit(self.main_menu_background, (0, 0))
            dark_overlay = pygame.Surface((800, 600))
            dark_overlay.set_alpha(128)  # Adjust the alpha value to control the darkness
            dark_overlay.fill((0, 0, 0))
            self.screen.blit(self.start_button, (300, 300))
            self.draw_text('Press Q to Quit', self.small_font, (255, 255, 255), self.screen, 300, 450)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.character_select()
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if 300 <= mouse_pos[0] <= 500 and 300 <= mouse_pos[1] <= 400:
                        self.character_select()

            pygame.display.flip()
            self.clock.tick(30)

    def character_select(self):
        selected = [False, False]
        pygame.mixer.music.load("sounds/characterselectBG.wav")
        pygame.mixer.music.play(-1)
        self.voice_line.play()

        while True:
            self.screen.blit(self.background, (0, 0))
            dark_overlay = pygame.Surface((800, 600))
            dark_overlay.set_alpha(128)  # Adjust the alpha value to control the darkness
            dark_overlay.fill((0, 0, 0))
            self.screen.blit(dark_overlay, (0, 0))

            self.draw_text('Character Select', self.font, (255, 255, 255), self.screen, 186, 50)
            self.draw_text(f'Player 1: {"Selected" if selected[0] else "Select"}', self.small_font, (255, 255, 255), self.screen, 100, 150)
            self.draw_text(f'Player 2: {"Selected" if selected[1] else "Select"}', self.small_font, (255, 255, 255), self.screen, 500, 150)
            if selected[0] and selected[1]:
                self.screen.blit(self.play_button, (300, 400))
            else:
                self.draw_text('Press Confirm your characters to play', self.small_font, (255, 255, 255), self.screen, 180, 500)

            # Display current wizard images
            self.screen.blit(self.wizzL_images[self.wizzL_index], (115, 200))
            self.screen.blit(self.wizzR_images[self.wizzR_index], (520, 200))

            # Display arrows
            self.screen.blit(self.arrow_left, (70, 235))
            self.screen.blit(self.arrow_right, (250, 235))
            self.screen.blit(self.arrow_left, (470, 235))
            self.screen.blit(self.arrow_right, (650, 235))

            # Display confirm buttons
            self.screen.blit(self.confirm_button, (140, 350))
            self.screen.blit(self.confirm_button, (540, 350))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if 70 <= mouse_pos[0] <= 120 and 235 <= mouse_pos[1] <= 285:
                        if not selected[0]:
                            self.wizzL_index = (self.wizzL_index - 1) % len(self.wizzL_images)
                    if 250 <= mouse_pos[0] <= 300 and 235 <= mouse_pos[1] <= 285:
                        if not selected[0]:
                            self.wizzL_index = (self.wizzL_index + 1) % len(self.wizzL_images)
                    if 470 <= mouse_pos[0] <= 520 and 235 <= mouse_pos[1] <= 285:
                        if not selected[1]:
                            self.wizzR_index = (self.wizzR_index - 1) % len(self.wizzR_images)
                    if 650 <= mouse_pos[0] <= 700 and 235 <= mouse_pos[1] <= 285:
                        if not selected[1]:
                            self.wizzR_index = (self.wizzR_index + 1) % len(self.wizzR_images)
                    if 140 <= mouse_pos[0] <= 240 and 350 <= mouse_pos[1] <= 400:
                        if not selected[0]:
                            self.selected_characters[0] = self.wizzL_images[self.wizzL_index]
                            selected[0] = True
                    if 540 <= mouse_pos[0] <= 640 and 350 <= mouse_pos[1] <= 400:
                        if not selected[1]:
                            self.selected_characters[1] = self.wizzR_images[self.wizzR_index]
                            selected[1] = True
                    if 300 <= mouse_pos[0] <= 500 and 400 <= mouse_pos[1] <= 580:
                        if selected[0] and selected[1]:
                            self.start_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

            pygame.display.flip()
            self.clock.tick(30)

    def start_game(self):
        from game import Game
        game = Game(self.selected_characters)
        game.play()

if __name__ == "__main__":
    menu = Menu()
    menu.main_menu()