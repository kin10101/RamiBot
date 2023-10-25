from ovos_tts_plugin_mimic3 import Mimic3TTSPlugin
import pygame

cfg = "en_US/cmu-arctic_low" #"en_UK/apope_low"  # select voice etc here

def speak(text):
    mimic = Mimic3TTSPlugin()
    mimic.get_tts(text, "mimic.wav", voice="en_US/cmu-arctic_low", speaker="slt")

    # Initialize the pygame mixer
    pygame.mixer.init()

    # Load the WAV file
    sound = pygame.mixer.Sound("mimic.wav")

    # Play the audio
    sound.play()

    # Convert the duration to an integer
    duration_in_ms = int(sound.get_length() * 1000)

    pygame.time.delay(duration_in_ms)

    pygame.quit()

speak("With a quizzical look, Perry, our astute observer, steps forward and gently probes, much like a wildlife researcher in the field, asking the fundamental question, What is happening? Why the congregation?")