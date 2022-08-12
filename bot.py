import sys
import logging

from cakechat import cakechat
from minitel import minitel

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
        self.cmds = {
            'mood': self.cmd_mood,
            'nick': self.cmd_nick,
            'botname': self.cmd_botname,
            'reset': self.cmd_reset,
            'quit': self.cmd_quit
        }

    def cmd_nick(self, params):
        if not params:
            return

        self.name = ' '.join(params)

    def cmd_botname(self, params):
        if not params:
            return

        self.botname = ' '.join(params)

    def cmd_mood(self, params):
        if not params:
            self.sendCmdRet('No mood?!?')
            return

        mood = params[0]
        if self.chatbot.setMood(mood):
            self.sendCmdRet(f'Mood changed to {mood}')
        else:
            self.sendCmdRet(f'Cannot change mood to unknown "{mood}"')

    def cmd_reset(self, params):
        self.reset()
        return True

    def cmd_quit(self, params):
        self.sendCmdRet('Bye\r\nConnection closed.')
        sys.exit(0)

    def reset(self):
        self.chatbot.reset()
        self.minitel.reset()

    def parseCmd(self, cmd):
        elems = cmd.split(' ')
        if elems[0] in self.cmds:
            self.logger.info(f'got cmd {cmd}')
            return self.cmds[elems[0]](elems[1:])
        else:
            self.logger.info(f'got unknown cmd {cmd}')
            self.sendCmdRet(f'Uknown command {cmd}')

    def sendCmdRet(self, str):
        self.minitel.send(f'>> {str}\r\n')

    def run(self):
        # Main loop
        while True:
            str = self.minitel.readline(self.name)

            # Strings starting with # are commands
            if str[0] == '#':
                if self.parseCmd(str[1:]):
                    continue
            else:
                self.logger.info(f'got line: {str}')
                resp = self.chatbot.send(str)
                self.logger.info(f'got resp {resp}, sending to minitel')
                self.minitel.send(f'<{self.botname}> {resp}\r\n')
