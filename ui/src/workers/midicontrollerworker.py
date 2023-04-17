import threading
from kivy.event import EventDispatcher
from modules.midicontroller.midicontroller import MidiController

class MidiControllerWorker(EventDispatcher):
    """
        A worker thread that runs a midi polling loop.
    """
    def __init__(self, midi_controller: MidiController, **kwargs):
        self._thread = None
        self._stop_event = None
        self.midi_controller = midi_controller
        self.register_event_type('on_midi_event')
    def start(self) -> None:
        """Start the worker thread."""
        self._thread = threading.Thread(target=self._run_loop)
        self._thread.start()

    def stop(self) -> None:
        """Stop the worker thread."""
        self._stop_event.set()
        if self._thread is None:
            return
        # Notice that we are not joining the thread here.
        self._thread = None
    def _run_loop(self) -> None:
        """Run the polling  loop."""
        while self._stop_event is None:
            if self.midi_controller:
                try:
                    for midi_event in self.midi_controller.poll_midi_device():
                        self.dispatch('on_midi_event', midi_event)
                except Exception as e:
                    self.dispatch('on_error', e)
    def on_midi_event(self, *args) -> None:
        pass
    def on_error(self, error, *args) -> None:
        print(error)
        pass