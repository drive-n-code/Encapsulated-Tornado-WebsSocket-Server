from typing import Optional, Awaitable, Union
from tornado.websocket import WebSocketHandler


class Handler(WebSocketHandler):
    """
    Handler that handles a websocket channel
    """

    def open(self):
        """
        Client opens a websocket
        """
        print('new connection opened')

    def on_message(self, message: Union[str, bytes]) -> Optional[Awaitable[None]]:
        print('message received: %s' % message)
        # Reverse Message and send it back
        print('sending back message: %s' % message[::-1])
        self.write_message(message[::-1])
        return None

    def on_close(self):
        """
        Channel is closed
        """
        print('connection closed')

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def check_origin(self, origin):
        """
        Override the origin check if needed
        """
        return True
