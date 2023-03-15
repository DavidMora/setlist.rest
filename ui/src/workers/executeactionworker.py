import logging 
import asyncio
import threading
from kivy.event import EventDispatcher

class ExecuteActionWorker(EventDispatcher):
    """
        A worker thread that runs an asyncio event loop.
        The loop calls an async callback and waits for it to finish.
    """
    def __init__(self, **kwargs):
        super(ExecuteActionWorker, self).__init__()
        self._thread = None
        self._stop_event = None
        self.daw = None
    def start(self, actions: callable, args: list) -> None:
        """Start the worker thread."""
        self._stop_event = asyncio.Event()
        self._thread = threading.Thread(target=self._run_loop)
        self._thread.start()
        self.actions = actions
        self.action_args = args

    def _run_loop(self) -> None:
        """Run the asyncio event loop."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._execute_action())

    async def _execute_action(self) -> None:
        """Run the asyncio event loop once."""
        for index, action in enumerate(self.actions):
            try:
                await action(*self.action_args[index])
                await asyncio.sleep(0.5)
            except Exception as e:
                self.dispatch('on_error', e)
    def on_error(self, error, *args) -> None:
        logging.debug('unable to execute action: ', error)
    