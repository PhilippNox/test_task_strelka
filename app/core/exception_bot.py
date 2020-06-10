class BotExceptionNoUser(Exception):
    def __init__(self, where: str):
        self.where = where