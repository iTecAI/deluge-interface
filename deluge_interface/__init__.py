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
        self.status: TorrentStatus = self.get_status()
    
    def get_status(self) -> TorrentStatus:
        self.status = self.deluge._call("core.get_torrent_status", [self.id, []])
        return self.status

    @property
    def paused(self) -> bool:
        return self.status["paused"]
    
    def pause(self) -> None:
        self.deluge.pause_torrent(self.id)
        self.get_status()
    
    def resume(self) -> None:
        self.deluge.resume_torrent(self.id)
        self.get_status()

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
        """Add magnet URL

        Args:
            magnet (str): Magnet URI

        Returns:
            Torrent: Torrent object
        """
        return Torrent(self, self._call("core.add_torrent_magnet", [magnet, kwargs]))
    
    def add_torrent_from_url(self, url: str, headers: dict = None, **kwargs) -> Torrent:
        """Add torrent from URL to .torrent file

        Args:
            url (str): Url to Torrent
            headers (dict, optional): Dictionary of additional headers to pass. Defaults to None.

        Returns:
            Torrent: Torrent object
        """
        return Torrent(self, self._call("core.add_torrent_url", [url, kwargs, headers]))
    
    def add_torrent_from_file(self, *path, **kwargs) -> Torrent:
        """Add torrent from path
        
        Args:
            path (*str): Path or paths to join

        Returns:
            Torrent: Torrent object
        """
        conpath = os.path.join(*path)
        filename = os.path.split(conpath)[1]
        with open(conpath, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
            return Torrent(self, self._call("core.add_torrent_file", [filename, data, kwargs]))
    
    def remove_torrent(self, torrent_id: str, remove_data: bool = False) -> None:
        """Remove torrent with ID

        Args:
            torrent_id (str): Torrent ID to remove
            remove_data (bool, optional): Remove all torrent data on host. Defaults to False.
        """
        self._call("core.remove_torrent", [torrent_id, remove_data])
    
    def pause_torrent(self, torrent_id: str) -> None:
        """Pauses torrent

        Args:
            torrent_id (str): Torrent to pause
        """
        self._call("core.pause_torrent", [torrent_id])
    
    def resume_torrent(self, torrent_id: str) -> None:
        """Resume torrent

        Args:
            torrent_id (str): Torrent to resume
        """
        self._call("core.resume_torrent", [torrent_id])
    
    def list_torrents(self) -> list[Torrent]:
        """List all current torrents

        Returns:
            list[Torrent]: List of Torrent objects
        """
        result_raw = self._call("core.get_session_state", [])
        return map(lambda i: Torrent(self, i), result_raw)

