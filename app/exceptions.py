class UserAlreadyExistsException(Exception):
    pass


class UserDoesNotExist(Exception):
    pass


class InvalidPasswordException(Exception):
    pass


class UserCannotMarkItselfAsSpamException(Exception):
    pass


class UserHasAlreadyMarkedThisContactAsSpamException(Exception):
    pass
