import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.load_sounds()

    def load_sounds(self):
        sound_files = {
            'bg_music': 'assets/sounds/bg_music.mp3',
            'plate': 'assets/sounds/Broken plates.wav',
            'bird': 'assets/sounds/Drill Gear.mp3',
            'laser': 'assets/sounds/Laser Gun.wav'
        }

        for name, path in sound_files.items():
            try:
                sound = pygame.mixer.Sound(path)
                if name != 'bg_music':
                    sound.set_volume(0.2)
                self.sounds[name] = sound
            except pygame.error as e:
                print(f"Error loading sound {path}: {e}")

        if 'bg_music' in self.sounds:
            pygame.mixer.music.load(sound_files['bg_music'])

    def play_music(self, loop=True):
        pygame.mixer.music.play(-1 if loop else 0)

    def play_sound(self, name):
        if name in self.sounds:
            self.sounds[name].play()