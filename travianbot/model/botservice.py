import threading

from .statemachine import StateMachine

from travianapi import account


class BotService(StateMachine):
    """ Обьединяет функции управления отдельным аккаунтом """

    def __init__(self, settings: dict):
        super(BotService, self).__init__()

        self.settings = settings
        self.url = settings['url']
        self.name = settings['username']
        self.password = settings['password']
        self.headers = settings['headers']

        self.account = None

        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

    def close(self) -> None:
        """ Закрывает сервис - останавливает управление за аккаунтом """
        print('service', id(self), 'close')

    def run(self) -> None:
        """ Функция выполняется в новом потоке. Управляет аккаунтом """
        from time import sleep
        self.account = account.Account(self.url, self.name, self.password, self.headers)
        while True:
            print('Bot service', id(self), 'step')
            sleep(3)
