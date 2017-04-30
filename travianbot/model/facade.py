from . import botservice


class Model:
    """ Обьединяет функции управления аккаунтом и обработку данных """

    def __init__(self):
        self.services = []
        self.current_service = None

    def open_service(self, settings: dict) -> None:
        """ Открывает новый сервис - управление новым аккаунтом """
        service = botservice.BotService(settings)
        self.services.append(service)

    def close_service(self, service: botservice.BotService) -> None:
        """ Закрывает указанный сервис """
        service.close()
        if service == self.current_service:
            self.current_service = None

    def start_service(self):
        pass
