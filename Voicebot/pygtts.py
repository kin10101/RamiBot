from gtts import gTTS
import pygame

def speak(text, lang='en'):
    # Create a gTTS object
    tts = gTTS(text, lang=lang)

    # Save the speech as an audio file
    tts.save("output.mp3")

    # Initialize the audio player
    pygame.mixer.init()
    sound = pygame.mixer.Sound("output.mp3")

    # Play the speech
    sound.play()
    # Wait for the speech to finish
    pygame.time.delay(int(sound.get_length() * 1000))
    pygame.quit()

print("imported from pyggts") #track imports

def playAudioFile(file):
    pygame.mixer.init()
    sound = pygame.mixer.Sound(file)
    sound.play()
    pygame.time.delay(int(sound.get_length() * 1000))
    pygame.quit()
