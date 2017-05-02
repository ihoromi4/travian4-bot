import threading
import queue

import observer

from .statemachine import StateMachine

from travianapi import account
from . import restransfer
from . import service

QUEUE_LIMIT = 0


class BotService(service.Service, StateMachine):
    """ Обьединяет функции управления отдельным аккаунтом """

    def __init__(self, settings: dict):
        service.Service.__init__(self)
        super(StateMachine, self).__init__()

        self.is_open = True

        self.settings = settings
        self.url = settings['url']
        self.name = settings['username']
        self.password = settings['password']
        self.headers = settings['headers']

        self.account = None
        self.resource_transfer = None

        self.start_service_thread(self.run)

        self.f()

    def close(self) -> None:
        """ Закрывает сервис - останавливает управление аккаунтом """

        self.is_open = False
        print('service', id(self), 'close')

    @service.transmitter
    def f(self):
        print('some func')

    def run(self) -> None:
        """ Функция выполняется в новом потоке. Управляет аккаунтом """

        from time import sleep

        self.account = account.Account(self.url, self.name, self.password, self.headers)
        self.resource_transfer = restransfer.ResourceTransferNet(self.account, {})

        while self.is_open:
            print('Bot service', id(self), 'step')
            self.handle_orders()
            self.resource_transfer.update()
            sleep(3)
