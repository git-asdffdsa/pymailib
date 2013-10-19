__author__ = 'asdffdsa'

class pymailliberror(BaseException):
    pass

class settings_not_right(pymailliberror):
    pass

class password_not_right(pymailliberror):
    pass

class settings_not_guessed(pymailliberror):
    pass

class settings_not_found(pymailliberror):
    pass

class server_not_reachable(pymailliberror):
    pass

class login_not_possible(pymailliberror):
    pass
