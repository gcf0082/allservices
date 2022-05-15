from flask import Flask
from blueprints.plugin_manage.plugin_manage_blueprint import plugin_manage_blueprint
from core import plugin_manage

import asyncio
import socketio
import pty
import os
import subprocess
import select
import termios
import struct
import fcntl
import shlex
import logging
import sys
import argparse

app = Flask(__name__)
app.register_blueprint(plugin_manage_blueprint)

sio = socketio.Client(logger=True, engineio_logger=True)
config_fd = None
config_child_pid = None

def set_winsize(fd, row, col, xpix=0, ypix=0):
    logging.debug("setting window size with termios")
    winsize = struct.pack("HHHH", row, col, xpix, ypix)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, winsize)

def read_and_forward_pty_output():
    global config_fd
    max_read_bytes = 1024 * 20
    while True:
        sio.sleep(0.01)
        #print('===>')
        if config_fd:
            #print('config_fd ok')
            timeout_sec = 0
            (data_ready, _, _) = select.select([config_fd], [], [], timeout_sec)
            if data_ready:
                output = os.read(config_fd, max_read_bytes).decode()
                print('xxx')
                sio.emit("pty-output", {"output": output}, namespace="/master_agent")
@sio.on("pty-input", namespace="/master_agent")
def pty_input(data):
    global config_fd
    """write to the child pty. The pty sees this as if you are typing in a real
    terminal.
    """
    if config_fd:
        logging.debug("received input from browser: %s" % data["input"])
        os.write(config_fd, data["input"].encode())


@sio.on('resize', namespace='/master_agent')
def resize(data):
    if config_fd:
        logging.debug(f"Resizing window to {data['rows']}x{data['cols']}")
        set_winsize(config_fd, data["rows"], data["cols"])


@sio.on("connect", namespace="/master_agent")
def connect():
    global config_child_pid
    global config_cmd
    global config_fd
    logging.info("new client connected")
    logging.error(config_child_pid)
    if config_child_pid:
        # already started child process, don't start another
        return

    # create child process attached to a pty we can read from and write to
    (child_pid, fd) = pty.fork()
    if child_pid == 0:
        # this is the child process fork.
        # anything printed here will show up in the pty, including the output
        # of this subprocess
        subprocess.run(config_cmd)
    else:
        # this is the parent process fork.
        # store child fd and pid
        config_fd = fd
        config_child_pid = "child_pid"
        set_winsize(fd, 50, 50)
        cmd = " ".join(shlex.quote(c) for c in config_cmd)
        # logging/print statements must go after this because... I have no idea why
        # but if they come before the background task never starts
        sio.start_background_task(target=read_and_forward_pty_output)

        #logging.info("child pid is " + child_pid)
        logging.info(
            f"starting background task with command `{cmd}` to continously read "
            "and forward pty output to client"
        )
        logging.info("task started")

def start_server():
    sio.connect('http://192.168.101.52:3000', namespaces=['/master_agent'])
    #sio.wait()      

def main():
    print('entry main====')
    global config_child_pid
    if config_child_pid:
        print('===>return')
        return
    logging.basicConfig(
        format=">>%(levelname)s (%(funcName)s:%(lineno)s) %(message)s",
        stream=sys.stdout,
        level=logging.DEBUG,
    )    
    plugin_manage.load_plugins()
    global config_cmd
    config_cmd = ['bash'] # + shlex.split(args.cmd_args)    
    start_server()
    print('============>')
    app.run(host='0.0.0.0', port=5000)    
if __name__ == "__main__":
    main()
