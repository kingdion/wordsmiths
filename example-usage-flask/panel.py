from __future__ import print_function
from wordsmiths.transform import OT_String
import sys
import sqlite3
import os
import json

from ast import literal_eval
from functools import wraps
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect, send

app = Flask(__name__)
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY = 'secret!',
))

# Eventlet ASYNC Server
# Pushes SocketIO for WebSocket usage
async_mode = "eventlet"
socketio = SocketIO(app, async_mode=async_mode)

@app.route('/')
def enter_site():
    return render_template('index.html')

@socketio.on('transform')
def commit_transform(operations):
    if str(operations['op1_type']) == "Insert":
        op1 = [{"retain": int(operations['op1_index'])}, {"insert": str(operations['op1_string'])}]
    if str(operations['op1_type']) == "Delete":
        op1 = [{"retain": int(operations['op1_index'])}, {"delete": int(operations['op1_string'])}]

    if str(operations['op2_type']) == "Insert":
        op2 = [{"retain": int(operations['op2_index'])}, {"insert": str(operations['op2_string'])}]
    if str(operations['op2_type']) == "Delete":
        op2 = [{"retain": int(operations['op2_index'])}, {"delete": int(operations['op2_string'])}]

    OT = OT_String("verbose")

    new_ops = OT.transform(op1, op2)
    emit('new_ops', {'op1': str(op1), 'op2': str(op2), 'op1_prime': str(new_ops[0]), 'op2_prime': str(new_ops[1])})
    emit('apply_original', {'op1_index': int(op1[0]['retain']), 'op1_string': str(op1[1]['insert']), 'op2_index': int(op2[0]['retain']), 'op2_string': str(op2[1]['insert'])})
    emit('apply_transformed', {'op1_index': int(operations['op1_index']), 'op1_string': str(operations['op1_string']), 'op2_index': int(operations['op2_index']), 'op2_string': str(operations['op2_string'])})

if __name__ == '__main__':
    socketio.run(app, debug=True)
