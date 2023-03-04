import logging 
import asyncio
import threading
from kivy.event import EventDispatcher
from modules.reacontrol.reacontrol import ReaControl

class StatusLoopWorker(EventDispatcher):
    """
        A worker thread that runs an asyncio event loop.
        The loop gathers status and marker information from the DAW.
        The loop is stopped by calling the stop() method.
        The loop stops automatically if there's an error.
    """
    def __init__(self, **kwargs):
        super(StatusLoopWorker, self).__init__()
        self._thread = None
        self._stop_event = None
        self.daw = None
        self.sleep_time = kwargs.get('sleep_time', 5)
        self.register_event_type('on_status')
        self.register_event_type('on_error')
        self.register_event_type('on_markers')
    def start(self, daw: ReaControl) -> None:
        """Start the worker thread."""
        if not self.daw:
            self.daw = daw
        self._stop_event = asyncio.Event()
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
        """Run the asyncio event loop."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._run_forever())

    async def _run_forever(self) -> None:
        """Run the asyncio event loop forever."""
        while not self._stop_event.is_set():
            if self.daw:
                try:
                    status = await self.daw.get_status()
                    self.dispatch('on_status', status)
                    markers = await self.daw.get_markers()
                    self.dispatch('on_markers', markers)
                except Exception as e:
                    self.dispatch('on_error', e)
            await asyncio.sleep(self.sleep_time)

    def on_status(self, *args) -> None:
        pass
    def on_markers(self, *args) -> None:
        pass
    def on_error(self, error, *args) -> None:
        logging.debug('unable to conncet to daw: ', error)
        self.stop()
    
