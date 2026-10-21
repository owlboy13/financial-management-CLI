from .auth import authentication
import logging

log = logging.getLogger(__name__)

class Login:
    def __init__(self, username, password):
        self.__username = username
        self.__password = password
        self.connected: bool = False

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value):
        if isinstance(value, str) and value:
            return self.username
        raise TypeError("Username precisa ser uma String")

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        if not isinstance(value, str) and value:
            return self.password

        raise TypeError("Password precisa ser uma String")


    def try_connected(self):
        try:
            auth = authentication(self.username, self.password)

            if not auth:
                log.error("[LOGIN] USERNAME OU PASSWORD INCORRETAS")
                return None

            log.info("LOGIN FEITO COM SUCESSO")
            self.connected = True
            return self.connected

        except ValueError as e:
            log.exception(f"[LOGIN] - VALOR ERRADO: {e}")

            

            
    
