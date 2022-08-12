import serial
import logging

class minitel:
    def __init__(self, device):
        self.ser = serial.Serial(device, 4800, timeout=60,
                bytesize=serial.SEVENBITS, parity=serial.PARITY_EVEN,
                stopbits=serial.STOPBITS_ONE)

        self.logger = logging.getLogger('minitelbot')

    def clearscr(self):
        # Clear screen, set cursor to 0,0
        clr = b'\x1B[2J\x1B[H\r'
        self.ser.write(clr)

    def reset(self):
        self.clearscr()
        self.ser.write(b'\x1B[7mWelcome to 3615 SOLO\x1B[0m\r\n')

    def send(self, str):
        self.ser.write(str.encode('ascii'))

    def readline(self, prompt):
        str = ''
        self.send(f'<{prompt}> ')

        while True:
            c = self.ser.read(1)
            if not c: # read timeout, we didn't type anything
                continue

            # Enter => send message
            if c == b'\r':
                self.ser.write(b'\r\n...\r')
                break
            # Special chars
            elif c == b'\x1B':
                code = self.ser.read(2)
                self.logger.debug(f'got escape char {code}')
                if code == b'Ol' or code == b'OR': # Correction or Retour
                    if str:
                        self.logger.debug(f'correction')
                        str = str[:-1]
                        self.ser.write(b'\x1B[1D \x1B[1D')
                elif code == b'OM': # Envoi (= same as enter)
                    self.ser.write(b'\r\n...\r')
                    break
            # Normal char
            else:
                str += c.decode('ascii')
                self.ser.write(c)
                self.logger.debug(f'got char {c}')

        return str
