class BadAuthenticationError(Exception):
    """Incorrect given authentication informations"""
    def __init__(self, *args: object) -> None:
        super().__init__("Authentication informations given are incorrect", *args)
