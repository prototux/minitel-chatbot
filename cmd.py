import sys
import logging

class cmd:
    def __init__(self, bot):
        self.cmdchar = '/'
        self.bot = bot

        self.logger = logging.getLogger('minitelbot')

        # Define built-in commands
        self.cmds = {
            'mood': self.cmd_mood,
            'nick': self.cmd_nick,
            'botname': self.cmd_botname,
            'reset': self.cmd_reset,
            'quit': self.cmd_quit
        }

    def exec(self, cmd):
        elems = cmd.split(' ')
        if elems[0] in self.cmds:
            self.logger.info(f'got cmd {cmd}')
            return self.cmds[elems[0]](elems[1:])
        else:
            self.logger.info(f'got unknown cmd {cmd}')
            self.send(f'Uknown command {cmd}')

    def send(self, str):
        self.bot.send(f'>> {str}\r\n')

    def cmd_nick(self, params):
        if not params:
            return
        self.bot.name = ' '.join(params)

    def cmd_botname(self, params):
        if not params:
            return
        self.bot.botname = ' '.join(params)

    def cmd_mood(self, params):
        if not params:
            self.send('No mood?!?')
            return

        mood = params[0]
        if self.bot.chatbot.setMood(mood):
            self.send(f'Mood changed to {mood}')
        else:
            self.send(f'Cannot change mood to unknown "{mood}"')

    def cmd_reset(self, params):
        self.bot.reset()
        return True

    def cmd_quit(self, params):
        self.send('Bye\r\nConnection closed.')
        sys.exit(0)
