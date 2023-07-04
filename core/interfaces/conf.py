import typing
from abc import abstractmethod


class ConfigProtocol(typing.Protocol):
    @abstractmethod
    def get(self, key: str, value: typing.Optional[typing.Any] = None) -> typing.Any:
        ...

    @abstractmethod
    def set(self) -> None:
        ...

    @abstractmethod
    def get_server(self) -> str:
        ...

    @abstractmethod
    def get_token(self) -> str:
        ...

    @abstractmethod
    def get_project_id(self) -> str:
        ...

    @abstractmethod
    def get_cli_overwrite(self) -> typing.Dict:
        ...
