import pygame
import sys
import os
import cv2
import mediapipe as mp
import time

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
        self.wand_image = pygame.transform.scale(pygame.image.load("visuals/wandcursor.png").convert_alpha(), (50, 50))  # Load and scale the wand image

        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
        self.mp_drawing = mp.solutions.drawing_utils

        self.click_cooldown = 0.5  # Cooldown period in seconds
        self.last_click_time = 0

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def main_menu(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(frame_rgb)

            hand_landmarks = None
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

            self.screen.blit(self.main_menu_background, (0, 0))
            dark_overlay = pygame.Surface((800, 600))
            dark_overlay.set_alpha(128)  
            dark_overlay.fill((0, 0, 0))
            self.screen.blit(self.start_button, (300, 300))
            self.draw_text('Press Q to Quit', self.small_font, (255, 255, 255), self.screen, 300, 450)

            if hand_landmarks:
                index_finger_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
                x, y = int(index_finger_tip.x * 800), int(index_finger_tip.y * 600)

                # Draw wand cursor
                wand_rect = self.wand_image.get_rect(center=(x, y))
                self.screen.blit(self.wand_image, wand_rect.topleft)

                # Check if the hand is over the start button
                if 300 <= x <= 500 and 300 <= y <= 400:
                    cv2.rectangle(frame, (300, 300), (500, 400), (0, 255, 0), 2)
                    if self.is_click(index_finger_tip, thumb_tip):
                        self.character_select()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cap.release()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.character_select()
                    if event.key == pygame.K_q:
                        cap.release()
                        pygame.quit()
                        sys.exit()

            pygame.display.flip()
            self.clock.tick(30)

    def is_click(self, index_finger_tip, thumb_tip):
        current_time = time.time()
        if current_time - self.last_click_time < self.click_cooldown:
            return False

        distance = ((index_finger_tip.x - thumb_tip.x) ** 2 + (index_finger_tip.y - thumb_tip.y) ** 2) ** 0.5
        if distance < 0.05:  # Adjust the threshold as needed
            self.last_click_time = current_time
            return True
        return False

    def character_select(self):
        selected = [False, False]
        pygame.mixer.music.load("sounds/characterselectBG.wav")
        pygame.mixer.music.play(-1)
        self.voice_line.play()

        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(frame_rgb)

            hand_landmarks = None
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

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

            if hand_landmarks:
                index_finger_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
                x, y = int(index_finger_tip.x * 800), int(index_finger_tip.y * 600)

                # Draw wand cursor
                wand_rect = self.wand_image.get_rect(center=(x, y))
                self.screen.blit(self.wand_image, wand_rect.topleft)

                # Check for interactions with the UI elements
                if 70 <= x <= 120 and 235 <= y <= 285:
                    if self.is_click(index_finger_tip, thumb_tip) and not selected[0]:
                        self.wizzL_index = (self.wizzL_index - 1) % len(self.wizzL_images)
                if 250 <= x <= 300 and 235 <= y <= 285:
                    if self.is_click(index_finger_tip, thumb_tip) and not selected[0]:
                        self.wizzL_index = (self.wizzL_index + 1) % len(self.wizzL_images)
                if 470 <= x <= 520 and 235 <= y <= 285:
                    if self.is_click(index_finger_tip, thumb_tip) and not selected[1]:
                        self.wizzR_index = (self.wizzR_index - 1) % len(self.wizzR_images)
                if 650 <= x <= 700 and 235 <= y <= 285:
                    if self.is_click(index_finger_tip, thumb_tip) and not selected[1]:
                        self.wizzR_index = (self.wizzR_index + 1) % len(self.wizzR_images)
                if 140 <= x <= 240 and 350 <= y <= 400:
                    if self.is_click(index_finger_tip, thumb_tip) and not selected[0]:
                        self.selected_characters[0] = self.wizzL_images[self.wizzL_index]
                        selected[0] = True
                if 540 <= x <= 640 and 350 <= y <= 400:
                    if self.is_click(index_finger_tip, thumb_tip) and not selected[1]:
                        self.selected_characters[1] = self.wizzR_images[self.wizzR_index]
                        selected[1] = True
                if 300 <= x <= 500 and 400 <= y <= 580:
                    if self.is_click(index_finger_tip, thumb_tip) and selected[0] and selected[1]:
                        cap.release()
                        self.start_game()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cap.release()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        cap.release()
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