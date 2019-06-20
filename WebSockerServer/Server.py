from WebSockerServer.Handler import Handler


class Server:
    __handler__ = None
    __server_port__ = None
    __server_address__ = None
    __http_server__ = None
    __instance__ = None
    __debug_mode__ = False
    __server_paths__ = [(r'/', Handler, {})]

    def __init__(self, paths=None) -> None:
        super().__init__()
        if paths is not None:
            self.__server_paths__ = paths
        self.initialize()

    def __del__(self):
        self.stop()

    def __load_env_file__(self, file_path: str, filename: str = '.env'):
        from dotenv import load_dotenv
        from pathlib import Path
        from os import getenv

        load_dotenv(Path(file_path) / filename)
        self.__set_debug_mode__(getenv('DEBUG'))
        self.set_server_port(getenv('WS_PORT'))
        self.set_server_address(getenv('WS_HOST'))

    def initialize(self, path_to_env_file: str = '.'):
        from tornado.web import Application
        from tornado.httpserver import HTTPServer

        self.__load_env_file__(path_to_env_file)
        if not self.__required_parameters_are_set__():
            raise Exception('required parameters are not present')

        self.__handler__ = Application(self.__server_paths__, debug=self.__debug_mode__)
        self.__http_server__ = HTTPServer(self.__handler__)

    def start(self):
        from tornado.ioloop import IOLoop

        self.__http_server__.listen(self.__server_port__, self.__server_address__)
        self.__instance__ = IOLoop.instance()
        self.__instance__.start()

    def stop(self):
        if self.__instance__:
            self.__instance__.stop()
            self.__http_server__.close_all_connections()
            self.__http_server__.stop()
            self.__instance__ = None

    def __required_parameters_are_set__(self):
        if self.__server_address__ is None:
            return False
        if self.__server_port__ is None:
            return False
        return True

    def __set_debug_mode__(self, value: str = 'False'):
        self.__server_port__ = value is not None and value == 'True'

    def set_server_port(self, port: int):
        self.__server_port__ = port

    def set_server_address(self, address: str):
        self.__server_address__ = address
