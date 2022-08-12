#!/usr/bin/env python3

import requests
import serial
import sys

if not sys.argv[1]:
    print('Usage: python chatbot.py <device>')
    sys.exit(1)

# Open the minitel, 4800 bauds at 7E1
ser = serial.Serial(sys.argv[1], 4800, timeout=60,
        bytesize=serial.SEVENBITS, parity=serial.PARITY_EVEN,
        stopbits=serial.STOPBITS_ONE)

# Do a request to cakechat
history = []
mood = 'neutral'
def chat(str):
    if len(history) == 3:
        history.pop(0)
    history.append(str)
    print(f'sending to cakechat with context {history}')

    url = 'http://localhost:8080/cakechat_api/v1/actions/get_response'
    body = {'context': history, 'emotion': mood}
    response = requests.post(url, json=body)
    print(response.json())
    return response.json().get('response', 'sorry, i didnt understand')

# Clear scren and say hello
clr = b'\x1B[2J\x1B[H\r'
ser.write(clr)
ser.write(b'\x1B[7mWelcome to 3615 CHAT\x1B[0m\r\n')

# Main loop
while True:
    print('waiting for line')
    str = ''
    ser.write(b'<me> ')

    while True:
        c = ser.read(1)
        if not c:
            continue

        # Enter => send message
        if c == b'\r':
            ser.write(b'\r\n...\r')
            break
        # Special chars
        elif c == b'\x1B':
            code = ser.read(2)
            print(f'got escape char {code}')
            if code == b'Ol' or code == b'OR': # Correction or Retour
                print(f'correction')
                str = str[:-1]
                ser.write(b'\x1B[1D \x1B[1D')
            elif code == b'OM': # Envoi (= same as enter)
                ser.write(b'\r\n...\r')
                break
        # Normal char
        else:
            str += c.decode('ascii')
            ser.write(c)
            print(f'got chat {c}')

    # Strings starting with # are commands
    if str[0] == '#':
        cmd = str[1:]
        print(f'got cmd {cmd}')
        if cmd == 'joy':
            mood = 'joy'
            ser.write(b'>> Mood changed to joyful\r\n')
        elif cmd == 'neutral':
            mood = 'neutral'
            ser.write(b'>> Mood changed to neutral\r\n')
        else:
            txt = f'>> Uknown command {cmd}\r\n'
            ser.write(txt.encode('ascii'))
    else:
        print(f'got line: {str}')
        resp = chat(str)
        print(f'got resp {resp}, sending to minitel')
        msg = f'<mogmi> {resp}\r\n'
        ser.write(msg.encode('ascii'))
