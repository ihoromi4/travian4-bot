import queue
import threading


def transmitter(func):
    def shell(self, *args, **kwargs):
        if self.is_thread():
            func(self, *args, **kwargs)
        else:
            self.put_order(shell, args, kwargs)

    return shell


class Service:
    def __init__(self):
        self._queue = queue.Queue()
        self._thread = None
        self._ident = None

    def start_service_thread(self, thread_func):
        self._thread = threading.Thread(target=thread_func)
        self._thread.daemon = True
        self._thread.start()
        self._ident = self._thread.ident

    def is_thread(self):
        return self._ident == threading.get_ident()

    def put_order(self, func, args: list, kwargs: dict):
        self._queue.put((func, (self,) + args, kwargs))

    def handle_orders(self):
        while not self._queue.empty():
            func, args, kwargs = self._queue.get()
            func(*args, **kwargs)
