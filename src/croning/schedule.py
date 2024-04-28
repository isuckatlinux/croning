from typing import Callable, Any
from .scheduler import Scheduler


def schedule_function(
    cron_format: str | Callable[[], str], identificator: str | None = None
):

    def register(function: Callable[[], Any]):

        function_identificator: str = (
            function.__name__ if identificator is None else identificator
        )
        Scheduler().register_function(
            function=function,
            cron_format=cron_format,
            identificator=function_identificator,
        )

        def wrapped_function():

            return function()

        return wrapped_function

    return register


def execute_scheduler():

    Scheduler().execute_scheduler()
