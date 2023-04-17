import pygame
import pygame.midi
import modules.helpers.constants as constants

class MidiController:
    def __init__(self) -> None:
        self.is_connected = False
    def start(self):
        pygame.init()
        pygame.midi.init()
        self.is_connected = True
    def restart(self):
        self.is_connected = False
        if self.is_connected:
            pygame.midi.quit()
        self.start()
    def is_the_right_midi_input_device(self, device):
        return device[1] == constants.midi_device_name and device[2] == 1
    def is_device_connected(self):
        return self.is_connected
    def poll_midi_device(self):
        device_id = None
        device = None
        if not self.is_connected:
            return
        for i in range(pygame.midi.get_count()):
            if self.is_the_right_midi_input_device(pygame.midi.get_device_info(i)):
                device_id = i
        if device_id is not None:
            device = pygame.midi.Input(device_id)
        while device is not None:
            if device.poll():
                midi_events = device.read(10)
                midi_evs = pygame.midi.midis2events(midi_events, device_id)
                for m_e in midi_evs:
                    if m_e.data2 > 0:
                        yield m_e.data1
