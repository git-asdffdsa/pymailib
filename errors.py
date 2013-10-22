__author__ = 'asdffdsa'

class pymailiberror(BaseException):
    pass

class settings_not_right(pymailiberror):
    pass

class password_not_right(pymailiberror):
    pass

class settings_not_guessed(pymailiberror):
    pass

class settings_not_found(pymailiberror):
    pass

class server_not_reachable(pymailiberror):
    pass

class login_not_possible(pymailiberror):
    pass

class database_doesnt_support(pymailiberror):
    pass