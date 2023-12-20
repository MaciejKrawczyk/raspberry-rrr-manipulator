import queue
from threading import Thread, Event


class Worker:
    def __init__(self):
        self.command_queue = queue.Queue()
        self.feedback_queue = queue.Queue()
        self.stop_event = Event()
        self.thread = Thread(target=self._run, daemon=True)

    def start(self):
        self.stop_event.clear()
        self.thread.start()

    def _run(self):
        while not self.stop_event.is_set():
            try:
                command = self.command_queue.get(timeout=1)
                feedback = f"Processed: {command}"
                self.feedback_queue.put(feedback)
            except queue.Empty:
                continue

    def add_command(self, command):
        self.command_queue.put(command)

    def get_feedback(self):
        return self.feedback_queue.get()
