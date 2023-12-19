#from ovos_tts_plugin_mimic3 import Mimic3TTSPlugin
import pygame

cfg = "en_US/cmu-arctic_low" #"en_UK/apope_low"  # select voice etc here

def speak(text):
    mimic = Mimic3TTSPlugin()
    mimic.get_tts(text, "mimic.wav", voice="en_US/cmu-arctic_low", speaker="slt")

    pygame.mixer.init()
    sound = pygame.mixer.Sound("mimic.wav")
    sound.play()
    pygame.time.delay(int(sound.get_length() * 1000))
    pygame.quit()


def playAudioFile(file):
    pygame.mixer.init()
    sound = pygame.mixer.Sound(file)
    sound.play()
    pygame.time.delay(int(sound.get_length() * 1000 + 500))
    pygame.quit()


playAudioFile("/home/kin/PycharmProjects/RamiBot/audio/activate.wav")