class FunctionAlreadyRegistered(KeyError):

    def __init__(self, function_identificator: str) -> None:
        super().__init__(f"Function {function_identificator} already registered!")
