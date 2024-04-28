from .singleton import Singleton
from typing import Callable, Any
from .exceptions import FunctionAlreadyRegistered
from croniter import croniter
from zoneinfo import ZoneInfo
from datetime import datetime


class Scheduler(metaclass=Singleton):

    def __init__(self) -> None:
        self.__function_callback: dict[str, Callable] = {}
        self.__cron_formats: dict[str, str | Callable[[], str]] = {}
        self.__current_zone_info: ZoneInfo | None = None
        self.__last_execution: dict[str, datetime] = {}

    @property
    def zone_info(self) -> ZoneInfo | None:
        return self.__current_zone_info

    @property
    def now(self) -> datetime:
        return datetime.now(tz=self.zone_info)

    def register_function(
        self,
        function: Callable[[], Any],
        cron_format: str | Callable[[], str],
        identificator: str,
    ):
        if identificator in self.__function_callback.keys():
            raise FunctionAlreadyRegistered(function_identificator=identificator)

        self.__function_callback[identificator] = function
        self.__cron_formats[identificator] = cron_format
        self.__last_execution[identificator] = self.now

    def get_cron(self, identificator: str) -> croniter:

        cron_format = self.__cron_formats[identificator]
        cron_format_parsed = cron_format() if callable(cron_format) else cron_format

        return croniter(
            cron_format_parsed,
            ret_type=datetime,
            start_time=self.__last_execution[identificator],
        )

    def next_execution(self, identificator: str) -> datetime:

        return self.get_cron(identificator=identificator).next()

    def execute_scheduler(self):

        while True:

            for identificator, function in self.__function_callback.items():
                next_execution = self.next_execution(identificator=identificator)
                if self.now >= next_execution:
                    self.__last_execution[identificator] = next_execution
                    function()
