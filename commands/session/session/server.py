#!/usr/bin/env python3
from flask import Flask, request
from .session import BashSession

app = Flask(__name__)

def session_route(command=None):
    if command:
        return '/session/id/<session>/'+command
    else:
        return '/session/id/<session>'

sessions = {}
def get_session(session, type=None):
    if session not in sessions:
        if type:
            sessions[session] = type()
        else:
            return None
    return sessions[session]

def remove_session(session):
    if session in sessions:
        del sessions[session]

@app.route(session_route('start'))
def start(session):
    s = get_session(session)
    if s:
        return "Session %s already exists!" % session
    s = get_session(session, type=BashSession)
    s.start()
    return ''

@app.route(session_route('stop'))
def stop(session):
    s = get_session(session)
    if not s:
        return "Session %s does not exist!" % session
    s.stop()
    remove_session(session)
    return ''

@app.route(session_route('kill'))
def kill(session):
    s = get_session(session)
    if not s:
        return "Session %s does not exist!" % session
    s.kill()
    remove_session(session)
    return ''

@app.route(session_route('execute'), methods=['PUT'])
def execute(session):
    s = get_session(session)
    if not s:
        return "Session %s does not exist!" % session
    command = request.form['command']
    r = s.execute(command.split('\n'))
    return '\n'.join(r)


if __name__ == '__main__':
    app.run(port=7007)
