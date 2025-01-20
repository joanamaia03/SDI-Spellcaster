import random
import pygame
from player import Player
from spell import Spell
from voiceSpell import recognize_speech
from reflex_test import perform_reflex_test
from menu import Menu

class Game:
    def __init__(self, selected_characters):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Spellcaster Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)  # Larger font for "You Win"
        self.players = [Player("Player 1"), Player("Player 2")]
        self.spells = [
            Spell("Fireball", 20, 10),
            Spell("Thunder", 25, 15),
            Spell("Rock", 15, 5),
            Spell("Ice", 10, 5),
            Spell("Magic Missile", 30, 20),
            Spell("Heal", -20, 10),
            Spell("Mana Charge", 0, -10),
            Spell("Kill", 99, 50)
        ]
        self.spell_sounds = {
            "Fireball": pygame.mixer.Sound("sounds/fireball.wav"),
            "Thunder": pygame.mixer.Sound("sounds/lightning.wav"),
            "Rock": pygame.mixer.Sound("sounds/rock.wav"),
            "Ice": pygame.mixer.Sound("sounds/ice.wav"),
            "Magic Missile": pygame.mixer.Sound("sounds/missile.wav"),
            "Heal": pygame.mixer.Sound("sounds/heal.wav"),
            "Mana Charge": pygame.mixer.Sound("sounds/charge.wav"),
            "Kill": pygame.mixer.Sound("sounds/Kill.wav"),
            "Fail": pygame.mixer.Sound("sounds/fail.wav")
        }
        self.background = pygame.image.load("visuals/background.jpg").convert()
        self.background = pygame.transform.scale(self.background, (800, 600))
        self.health_bar_image = pygame.image.load("visuals/health_bar.png").convert_alpha()
        self.mana_bar_image = pygame.image.load("visuals/mana_bar.png").convert_alpha()
        self.mana_bar_image = pygame.transform.scale(self.mana_bar_image, (180, 45))  # Scale the mana bar image
        self.spell_animations = {
            "Fireball": [pygame.transform.scale(pygame.image.load(f"visuals/fireballanim/tile{i}.png").convert_alpha(), (300, 300)) for i in range(0, 17)],
            "Thunder": [pygame.transform.scale(pygame.image.load(f"visuals/thunderanim/tile{i}.png").convert_alpha(),(200,200)) for i in range(0, 12)],
            "Rock": [pygame.transform.scale(pygame.image.load(f"visuals/rockanim/tile{i}.png").convert_alpha(),(200,200)) for i in range(0, 11)],
            "Ice": [pygame.transform.scale(pygame.image.load(f"visuals/iceanim/tile{i}.png").convert_alpha(),(400,400)) for i in range(0, 34)],
            "Magic Missile": [pygame.transform.scale(pygame.image.load(f"visuals/missleanim/tile{i}.png").convert_alpha(),(200,200)) for i in range(0, 15)],
            "Heal": [pygame.transform.scale(pygame.image.load(f"visuals/healanim/tile{i}.png").convert_alpha(),(200,200)) for i in range(0, 15)],
            "Mana Charge": [pygame.transform.scale(pygame.image.load(f"visuals/chargeanim/tile{i}.png").convert_alpha(),(200,200)) for i in range(0, 12)],
            "Kill": [pygame.transform.scale(pygame.image.load(f"visuals/killanim/tile{i}.png").convert_alpha(),(500,500)) for i in range(0, 21)],
            "Fail": [pygame.transform.scale(pygame.image.load(f"visuals/failanim/tile{i}.png").convert_alpha(), (200, 200)) for i in range(0, 10)] 
        }
        self.player_images = {
            "Player 1": pygame.transform.scale(selected_characters[0], (200, 200)),
            "Player 2": pygame.transform.scale(selected_characters[1], (200, 200)) 
        }
        self.player_positions = {
            "Player 1": (55, 300),  # Example position for Player 1
            "Player 2": (550, 300)   # Example position for Player 2
        }

        self.current_player = 0

        # Load and play background music
        pygame.mixer.music.load("sounds/bgmusic2.wav")
        pygame.mixer.music.play(-1)  # Play the music in a loop

        # Load pre-fight sound effects
        self.ready_sound = pygame.mixer.Sound("sounds/ready.wav")
        self.fight_sound = pygame.mixer.Sound("sounds/fight.wav")

        # Load pre-fight images
        self.ready_image = pygame.image.load("visuals/wizzardsready.png").convert_alpha()
        self.fight_image = pygame.image.load("visuals/fight.png").convert_alpha()

        # Load game over music
        self.game_over_music = "sounds/victory.wav"

    def next_turn(self):
        self.current_player = (self.current_player + 1) % 2

    def get_current_player(self):
        return self.players[self.current_player]

    def get_opponent(self):
        return self.players[(self.current_player + 1) % 2]

    def draw_health_bars(self):
        for i, player in enumerate(self.players):
            # Health bar
            health_bar_length = 195
            health_bar_height = 20
            health_ratio = player.health / 100
            health_bar_position = (50 + i * 400, 50)
            health_bar_position_img = (35 + i * 400, 30)
            pygame.draw.rect(self.screen, (255, 0, 0), (health_bar_position[0], health_bar_position[1], health_bar_length, health_bar_height))
            pygame.draw.rect(self.screen, (0, 255, 0), (health_bar_position[0], health_bar_position[1], health_bar_length * health_ratio, health_bar_height))
            self.screen.blit(self.health_bar_image, health_bar_position_img)

            # Mana bar
            mana_bar_length = 150
            mana_bar_height = 15
            mana_ratio = player.mana / 50
            mana_bar_position = (94 + i * 400, 90)
            mana_bar_position_img = (70 + i * 400, 75)
            pygame.draw.rect(self.screen, (150, 0, 150), (mana_bar_position[0], mana_bar_position[1], mana_bar_length, mana_bar_height))
            pygame.draw.rect(self.screen, (0, 0, 255), (mana_bar_position[0], mana_bar_position[1], mana_bar_length * mana_ratio, mana_bar_height))
            self.screen.blit(self.mana_bar_image, mana_bar_position_img)

    def draw_turn_info(self):
        current_player = self.get_current_player()
        text = self.font.render(f"{current_player.name}'s turn", True, (255, 255, 255))
        self.screen.blit(text, (300, 550))

    def draw_initial_ui(self):
        self.screen.blit(self.background, (0, 0))
        dark_overlay = pygame.Surface((800, 600))
        dark_overlay.set_alpha(128)  # Adjust the alpha value to control the darkness
        dark_overlay.fill((0, 0, 0))
        self.screen.blit(dark_overlay, (0, 0))
        for player_name, position in self.player_positions.items():
            self.screen.blit(self.player_images[player_name], position)
        self.draw_health_bars()
        self.draw_turn_info()
        pygame.display.flip()

    def play_spell_animation(self, spell_name, target_position):
        for frame in self.spell_animations[spell_name]:
            frame_rect = frame.get_rect(center=target_position)
            self.screen.blit(self.background, (0, 0))
            dark_overlay = pygame.Surface((800, 600))
            dark_overlay.set_alpha(128)  # Adjust the alpha value to control the darkness
            dark_overlay.fill((0, 0, 0))
            self.screen.blit(dark_overlay, (0, 0))
            self.draw_health_bars()
            self.draw_turn_info()
            for player_name, position in self.player_positions.items():
                self.screen.blit(self.player_images[player_name], position)
            self.screen.blit(frame, frame_rect.topleft)
            pygame.display.flip()
            self.clock.tick(10)  # Adjust the frame rate for the animation

    def pre_fight_sequence(self):
        # Display "Wizards Ready"
        self.screen.blit(self.background, (0, 0))
        dark_overlay = pygame.Surface((800, 600))
        dark_overlay.set_alpha(128)
        dark_overlay.fill((0, 0, 0))
        self.screen.blit(dark_overlay, (0, 0))
        ready_rect = self.ready_image.get_rect(center=(400, 300))
        self.screen.blit(self.ready_image, ready_rect.topleft)
        pygame.display.flip()
        self.ready_sound.play()
        pygame.time.wait(2000)  # Wait for 2 seconds

        # Display "Fight"
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(dark_overlay, (0, 0))
        fight_rect = self.fight_image.get_rect(center=(400, 300))
        self.screen.blit(self.fight_image, fight_rect.topleft)
        pygame.display.flip()
        self.fight_sound.play()
        pygame.time.wait(2000)  # Wait for 2 seconds

        # Clear the "Fight" image before starting the game
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(dark_overlay, (0, 0))
        for player_name, position in self.player_positions.items():
            self.screen.blit(self.player_images[player_name], position)
        self.draw_health_bars()
        self.draw_turn_info()
        pygame.display.flip()

    def game_over(self, winner):
        pygame.mixer.music.stop()  # Stop the background music
        pygame.mixer.music.load(self.game_over_music)
        pygame.mixer.music.play(-1)  # Play the game over music in a loop

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Press 'R' to restart
                        menu = Menu()
                        selected_characters = menu.main_menu()
                        self.__init__(selected_characters)  # Reinitialize the game with selected characters
                        self.play()
                        return
                    elif event.key == pygame.K_q:  # Press 'Q' to go back to character select
                        menu = Menu()
                        pygame.mixer.music.stop()  # Stop the background music
                        selected_characters = menu.character_select()
                        self.__init__(selected_characters)  # Reinitialize the game with selected characters
                        self.play()
                        return

            self.screen.blit(self.background, (0, 0))
            dark_overlay = pygame.Surface((800, 600))
            dark_overlay.set_alpha(128)
            dark_overlay.fill((0, 0, 0))
            self.screen.blit(dark_overlay, (0, 0))

            text = self.large_font.render("You Win!", True, (255, 255, 255))
            self.screen.blit(text, (300, 150))  # Adjusted position for "You Win"

            winner_image = self.player_images[winner.name]
            winner_rect = winner_image.get_rect(center=(400, 300))
            self.screen.blit(winner_image, winner_rect.topleft)

            text = self.font.render("Press 'R' to Restart or 'Q' to Character Select", True, (255, 255, 255))
            self.screen.blit(text, (150, 500))

            pygame.display.flip()
            self.clock.tick(30)

    def play(self):
        running = True
        self.draw_initial_ui()  # Draw the initial UI when the game starts

        self.pre_fight_sequence()  # Play the pre-fight sequence

        while running and all(player.is_alive() for player in self.players):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            current_player = self.get_current_player()
            opponent = self.get_opponent()
            print(f"{current_player.name}'s turn.")

            spell = None
            for _ in range(3):
                spell_name = recognize_speech()
                if spell_name:
                    spell = next((s for s in self.spells if s.name.lower() == spell_name.lower()), None)
                    if spell:
                        break
                print("Spell not recognized. Try again.")

            if spell:
                damage = current_player.cast_spell(spell)
                if damage == "fail":
                    print(f"{current_player.name} failed to cast {spell.name} due to insufficient mana.")
                    self.spell_sounds["Fail"].play()  # Play the fail sound
                    self.play_spell_animation("Fail", self.player_positions[current_player.name])  # Play the fail animation
                else:
                    if spell.name not in ["Heal", "Mana Charge"]:
                        opponent.take_damage(damage)
                        target_position = self.player_positions[opponent.name]  # Position on the opponent's side
                    else:
                        target_position = self.player_positions[current_player.name]  # Position on the current player's side
                    target_position = (target_position[0] + 100, target_position[1] + 100)  # Adjust to center of player
                    print(f"{current_player.name} casts {spell.name} on {opponent.name} for {damage} damage.")
                    self.spell_sounds[spell.name].play()  # Play the spell sound
                    self.play_spell_animation(spell.name, target_position)  # Play the spell animation
            else:
                print(f"{current_player.name} failed to cast a spell.")

            self.next_turn()

            # Draw everything
            self.screen.blit(self.background, (0, 0))
            dark_overlay = pygame.Surface((800, 600))
            dark_overlay.set_alpha(128)  # Adjust the alpha value to control the darkness
            dark_overlay.fill((0, 0, 0))
            self.screen.blit(dark_overlay, (0, 0))
            self.draw_health_bars()
            self.draw_turn_info()
            for player_name, position in self.player_positions.items():
                self.screen.blit(self.player_images[player_name], position)
            pygame.display.flip()
            self.clock.tick(30)

        winner = self.get_current_player() if self.get_current_player().is_alive() else self.get_opponent()
        self.game_over(winner)

if __name__ == "__main__":
    menu = Menu()
    selected_characters = menu.main_menu()
    game = Game(selected_characters)
    game.play()