#!/usr/bin/env python3

import argparse
from bot import bot

argsp = argparse.ArgumentParser()
argsp.add_argument('-n', '--name', action='store', help='Name of the bot', default='mogmi')
argsp.add_argument('-s', '--service', action='store', help='URL to cakechat service', default='localhost:8080')
argsp.add_argument('-d', '--device', action='store', help='Serial device for minitel', default='/dev/ttyUSB0')
args = argsp.parse_args()


bot(args.name, args.service, args.device).run()
