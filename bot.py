import sys
import logging

from cakechat import cakechat
from minitel import minitel
from cmd import cmd

class bot:
    def __init__(self, name, service, device):
        self.botname = name
        self.name = 'me'

        # Init minitel and cakechat
        self.minitel = minitel(device)
        self.chatbot = cakechat(service)

        # init logging
        self.logger = logging.getLogger('minitelbot')
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)

        # First reset
        self.reset()

        # Define built-in commands
        self.cmds = cmd(self)

    def reset(self):
        self.chatbot.reset()
        self.minitel.reset()

    def send(self, str):
        seld.minitel.send(str)

    def run(self):
        # Main loop
        while True:
            str = self.minitel.readline(self.name)

            # Manage commands if line starts with $cmdchar
            if str[0] == self.cmds.cmdchar:
                if self.cmds.exec(str[1:]):
                    continue
            else:
                self.logger.info(f'got line: {str}')
                resp = self.chatbot.send(str)
                self.logger.info(f'got resp {resp}, sending to minitel')
                self.minitel.send(f'<{self.botname}> {resp}\r\n')
