# minitel-chatbot
A minitel chatbot using python and cakechat, nothing special
It's a 3AM project, it's shitty, QnD code, just here to share for some friends.
Don't expect any actual use from this code

## Howto run

* `docker pull lukalabs/cakechat:latest`
* `docker run --name cakechat-server -p 127.0.0.1:8080:8080 -it lukalabs/cakechat:latest bash -c "python bin/cakechat_server.py"`
* wait quite some time for cakechat to run (you'll see flask logs)
* `pip install requests pyserial`
* `sudo python chatbot.py` (the sudo is due to the serial device, maybe you don't need sudo)

## What it does

Basically, a minimal IRC-like UI (ab)using VT100 escape codes that forwards messages to CakeChat, that's pretty much all
