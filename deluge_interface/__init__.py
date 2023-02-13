import requests
from typing import Any
import json
import base64
import os
from ._types import *

USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"

class DelugeException(ConnectionError):
    def __init__(self, code: int, message: str) -> None:
        super().__init__(f"Code {code} : {message}")

class AuthException(DelugeException):
    def __init__(self) -> None:
        super().__init__(-1, "Failed to authenticate.")

class Torrent:
    def __init__(self, deluge: "Deluge", torrent_id: str) -> None:
        self.deluge = deluge
        self.id = torrent_id
    
    def status(self) -> TorrentStatus:
        return self.deluge._call("core.get_torrent_status", [self.id, []])

class Deluge:
    JSON_PATH = "{host}/json"
    def __init__(self, host: str, password: str) -> None:
        """Initialize Deluge session

        Args:
            host (str): Full URL to server ("http(s)://example.com:port")
            password (str): User password
        """
        self.host: str = host
        self.call_id: int = 1
        self.session_id: str = None
        self.auth(password)
        self.methods: list[str] = self.get_methods()
    
    def _call_raw(self, command: str, parameters: list[Any]) -> requests.Response:
        """Helper function to call a RPC method

        Args:
            command (str): RPC command
            parameters (list[Any]): List of parameters

        Returns:
            requests.Response: Raw Response object
        """
        headers = {
            "Host": self.host.split("//")[1],
            "Origin": self.host,
            "User-Agent": USER_AGENT,
            "Content-Type": "application/json"
        }
        if self.session_id:
            headers["Cookie"] = f"_session_id={self.session_id}"
        resp = requests.post(self.JSON_PATH.format(host=self.host), headers=headers, data=json.dumps({
            "id": self.call_id,
            "method": command,
            "params": parameters
        }))
        return resp
    
    def _call(self, command: str, parameters: list[Any]) -> Any:
        """Helper function to call RPC methods

        Args:
            command (str): RPC method
            parameters (list[Any]): List of parameters

        Raises:
            DelugeException: Generic failure exception

        Returns:
            Any: Data from `result` key of response JSON
        """
        response = self._call_raw(command, parameters)
        data = response.json()
        if data["result"]:
            return data["result"]
        else:
            raise DelugeException(code=data["error"]["code"], message=data["error"]["message"])
    
    def auth(self, password: str):
        """Logs in to Deluge server

        Args:
            password (str): String password

        Raises:
            AuthException: Failed to authenticate
            DelugeException: Other error occurred
        """
        resp = self._call_raw("auth.login", [password])
        data = resp.json()
        if data["result"] != None:
            if data["result"]:
                headers = resp.headers
                if "Set-Cookie" in headers.keys():
                    self.session_id = headers["Set-Cookie"].split(";")[0].split("=")[1]
            else:
                raise AuthException()
        else:
            raise DelugeException(code=data["error"]["code"], message=data["error"]["message"])
    
    def get_methods(self) -> list[str]:
        """Returns all RPC methods

        Returns:
            list[str]: List of RPC methods
        """
        return self._call("system.listMethods", [])
    
    def add_magnet(self, magnet: str, **kwargs) -> Torrent:
        return Torrent(self, self._call("core.add_torrent_magnet", [magnet, kwargs]))
    
    def add_torrent_from_url(self, url: str, headers: dict = None, **kwargs) -> str:
        return Torrent(self, self._call("core.add_torrent_url", [url, kwargs, headers]))
    
    def add_torrent_from_file(self, *path, **kwargs) -> str:
        conpath = os.path.join(*path)
        filename = os.path.split(conpath)[1]
        with open(conpath, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
            return Torrent(self, self._call("core.add_torrent_file", [filename, data, kwargs]))

