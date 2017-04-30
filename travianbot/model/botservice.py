import threading
import queue

import observer

from .statemachine import StateMachine

from travianapi import account
from . import restransfer

QUEUE_LIMIT = 0


class BotService(StateMachine):
    """ Обьединяет функции управления отдельным аккаунтом """

    def __init__(self, settings: dict):
        super(StateMachine, self).__init__()

        self.orders = queue.Queue()
        self.is_open = True

        self.settings = settings
        self.url = settings['url']
        self.name = settings['username']
        self.password = settings['password']
        self.headers = settings['headers']

        self.account = None
        self.resource_transfer = None

        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

    def close(self) -> None:
        """ Закрывает сервис - останавливает управление за аккаунтом """

        self.is_open = False
        print('service', id(self), 'close')

    def run(self) -> None:
        """ Функция выполняется в новом потоке. Управляет аккаунтом """

        from time import sleep

        self.account = account.Account(self.url, self.name, self.password, self.headers)
        self.resource_transfer = restransfer.ResourceTransferNet(self.account, {})

        while self.is_open:
            print('Bot service', id(self), 'step')
            self.resource_transfer.update()
            sleep(3)
