import speech_recognition as sr
import pygame
import random
import math
import tkinter as tk
import threading
import cv2
import time
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize libraries
pygame.init()
pygame.mixer.init()

# Load sounds
spell_sounds = {
    "fireball": "fireball.wav",
    "thunder": "thunder.mp3",
    "rock": "rock.mp3",
    "ice": "ice.mp3",
    "magic missile": "missile.wav",
    "heal": "heal.mp3",
}

# Load visuals (example)
def draw_fireball(screen):
    for _ in range(50):
        x = random.randint(250, 350)
        y = random.randint(250, 350)
        size = random.randint(5, 15)
        pygame.draw.rect(screen, (255, 69, 0), (x, y, size, size))

def draw_lightning(screen):
    for _ in range(10):
        x = random.randint(290, 310)
        y = random.randint(200, 400)
        size = random.randint(5, 10)
        pygame.draw.rect(screen, (0, 191, 255), (x, y, size, size))

def draw_heal(screen):
    for _ in range(50):
        x = random.randint(225, 375)
        y = random.randint(225, 375)
        size = random.randint(5, 15)
        pygame.draw.rect(screen, (50, 205, 50), (x, y, size, size))

def draw_magic_missile(screen, frame):
    for _ in range(5):
        x = random.randint(250, 350)
        y = random.randint(250, 350)
        size = random.randint(5, 10)
        pygame.draw.rect(screen, (0, 0, 255), (x, y, size, size))

def draw_thunder(screen):
    for _ in range(10):
        x = random.randint(250, 350)
        y = random.randint(250, 350)
        size = random.randint(5, 15)
        pygame.draw.rect(screen, (255, 255, 0), (x, y, size, size))

def draw_rock(screen):
    for _ in range(50):
        x = random.randint(250, 350)
        y = random.randint(250, 350)
        size = random.randint(5, 15)
        pygame.draw.rect(screen, (139, 69, 19), (x, y, size, size))

def draw_ice(screen):
    for _ in range(50):
        x = random.randint(250, 350)
        y = random.randint(250, 350)
        size = random.randint(5, 15)
        pygame.draw.rect(screen, (173, 216, 230), (x, y, size, size))

visual_effects = {
    "fireball": draw_fireball,
    "magic missile": draw_magic_missile,
    "heal": draw_heal,
    "thunder": draw_thunder,
    "rock": draw_rock,
    "ice": draw_ice,
}

def hand_tracking(spell_queue):
    cap = cv2.VideoCapture(0)
    previous_spell = None

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                detected_spell = detect_hand_motion(hand_landmarks)
                if detected_spell and detected_spell != previous_spell:
                    spell_queue.append(detected_spell)
                    previous_spell = detected_spell
                    print(f"Detected spell: {detected_spell}")

        time.sleep(0.1)  # Add a small delay to avoid overwhelming the CPU

def detect_hand_motion(hand_landmarks):
    # Get the coordinates of the landmarks
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

    thumb_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP]
    index_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
    middle_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
    ring_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]
    pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]

    # Calculate distances to determine if fingers are extended
    def is_finger_extended(tip, mcp):
        return tip.y < mcp.y

    thumb_extended = is_finger_extended(thumb_tip, thumb_mcp)
    index_extended = is_finger_extended(index_tip, index_mcp)
    middle_extended = is_finger_extended(middle_tip, middle_mcp)
    ring_extended = is_finger_extended(ring_tip, ring_mcp)
    pinky_extended = is_finger_extended(pinky_tip, pinky_mcp)

    # Open hand (all fingers extended)
    if thumb_extended and index_extended and middle_extended and ring_extended and pinky_extended:
        return "ice"

    # Pointing finger (only index finger extended)
    if not thumb_extended and index_extended and not middle_extended and not ring_extended and not pinky_extended:
        return "thunder"

    # Closed hand (no fingers extended)
    if not thumb_extended and not index_extended and not middle_extended and not ring_extended and not pinky_extended:
        return "rock"

    # Peace sign (index and middle fingers extended)
    if not thumb_extended and index_extended and middle_extended and not ring_extended and not pinky_extended:
        return "heal"

    return None

# Initialize speech recognizer
recognizer = sr.Recognizer()


def listen_for_spell(mic_index, spell_queue):
    with sr.Microphone(device_index=mic_index) as source:
        while True:
            print("Listening for spell...")
            try:
                audio = recognizer.listen(source, timeout=5)
                command = recognizer.recognize_google(audio)
                print(f"You said: {command}")
                spell_queue.append(command.lower())
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
            except sr.WaitTimeoutError:
                print("Listening timed out while waiting for phrase to start")

# List available microphones
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"Microphone with index {index}: {name}")

# Replace with your desired microphone index
mic_index = 6  # Example index, replace with the correct one

def animate_effect(screen, effect_func, duration=1000, fps=30):
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    frame = 0
    while pygame.time.get_ticks() - start_time < duration:
        screen.fill((0, 0, 0))  # Clear the screen
        if effect_func in [draw_magic_missile]:
            effect_func(screen, frame)
        else:
            effect_func(screen)
        pygame.display.flip()
        clock.tick(fps)
        frame += 1

def run_spellcast_audio():
    pygame.init()  # Reinitialize Pygame
    pygame.mixer.init()

    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Spell Cast")

    spell_queue = []
    listener_thread = threading.Thread(target=listen_for_spell, args=(mic_index, spell_queue))
    listener_thread.daemon = True
    listener_thread.start()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Press ESC to go back to menu
                    running = False

        screen.fill((0, 0, 0))  # Clear the screen

        if spell_queue:
            spell = spell_queue.pop(0)
            if spell in visual_effects:
                pygame.mixer.Sound(spell_sounds[spell]).play()
                animate_effect(screen, visual_effects[spell])

        # Draw "Press ESC to exit" text with background rectangle
        font = pygame.font.Font(None, 36)
        text = font.render("Press ESC to go back to menu", True, (255, 255, 255))
        text_rect = text.get_rect(center=(300, 550))
        pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(20, 10))  # Background rectangle
        screen.blit(text, text_rect)

        pygame.display.flip()

    pygame.quit()
    show_menu()

def run_spellcast_video():
    pygame.init()  # Reinitialize Pygame
    pygame.mixer.init()

    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Spell Cast")

    spell_queue = []

    hand_tracking_thread = threading.Thread(target=hand_tracking, args=(spell_queue,))
    hand_tracking_thread.daemon = True
    hand_tracking_thread.start()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Press ESC to go back to menu
                    running = False

        screen.fill((0, 0, 0))  # Clear the screen

        if spell_queue:
            spell = spell_queue.pop(0)
            if spell in visual_effects:
                print(f"Playing spell: {spell}")  # Debugging print statement
                pygame.mixer.Sound(spell_sounds[spell]).play()
                animate_effect(screen, visual_effects[spell])
                time.sleep(0.5)  # Add a delay between spells

        # Draw "Press ESC to exit" text with background rectangle
        font = pygame.font.Font(None, 36)
        text = font.render("Press ESC to go back to menu", True, (255, 255, 255))
        text_rect = text.get_rect(center=(300, 550))
        pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(20, 10))  # Background rectangle
        screen.blit(text, text_rect)

        pygame.display.flip()

    pygame.quit()
    show_menu()

def start_program_audio():
    root.destroy()  # Close the Tkinter window
    run_spellcast_audio()

def start_program_video():
    root.destroy()  # Close the Tkinter window
    run_spellcast_video()

def quit_program():
    root.destroy()

def show_menu():
    global root
    root = tk.Tk()
    root.title("Spellcaster")
    root.geometry("640x350")

    # Load the background image
    bg_photo = tk.PhotoImage(file="mainmenu.png")
    bg_photo = bg_photo.subsample(3, 3)

    # Create a canvas and set the background image
    canvas = tk.Canvas(root, width=640, height=350)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    # Start Button
    start_buttonAudio = tk.Button(root, text="StartAudio", font=("Helvetica", 16), command=start_program_audio, bg="lightpink", fg="black", width=20)
    start_buttonVideo = tk.Button(root, text="StartVisual", font=("Helvetica", 16), command=start_program_video, bg="lightpink", fg="black", width=20)
    start_button_window1 = canvas.create_window(320, 205, window=start_buttonAudio)
    start_button_window2 = canvas.create_window(320, 255, window=start_buttonVideo)

    # Quit Button
    quit_button = tk.Button(root, text="Quit", font=("Helvetica", 16), command=quit_program, bg="blue", fg="white", width=20)
    quit_button_window = canvas.create_window(320,305, window=quit_button)

    # Run the Tkinter main loop
    root.mainloop()

# Show the menu when the program starts
show_menu()
