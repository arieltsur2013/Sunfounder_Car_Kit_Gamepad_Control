#!/usr/bin/env python
# -*- coding: utf-8 -*-

from socket import socket, AF_INET, SOCK_STREAM     # Import necessary modules
import time
import inputs

try:
    # Get pretty coloured text - $ pip install colored
    from colored import fg, bg, attr
except ImportError:
    # Fall-back to no colours:
    print("Psst! Type 'pip install colored' to get coloured output text")
    def fg(*args, **kwargs):
        return ''
    def bg(*args, **kwargs):
        return ''
    def attr(*args, **kwargs):
        return ''

connect_to_car=True

HOST = '192.168.1.31'    # Server(Raspberry Pi) IP address
PORT = 21567
BUFSIZ = 1024             # buffer size
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)   # Create a socket
if connect_to_car:
    tcpCliSock.connect(ADDR)                    # Connect with the server

def action(a):
    if connect_to_car:
        tcpCliSock.send(str.encode(a))

def y(state):
    if state == 0:
        print('{}↑ Forward!{}'.format(fg('blue'), attr('reset')))
        action('forward')
    elif state == 127:
        print('{}↕ Center!{}'.format(fg('blue'), attr('reset')))
        action('stop')
    elif state == 255:
        print('{}↓ Backwards!{}'.format(fg('blue'), attr('reset')))
        action('backward')

def x(state):
    if state == 0:
        print('{}← Left!{}'.format(fg('yellow'), attr('reset')))
        action('left')
    elif state == 127:
        print('{}↔ Center!{}'.format(fg('yellow'), attr('reset')))
        action('home')
    elif state == 255:
        print('{}→ Right!{}'.format(fg('yellow'), attr('reset')))
        action('right')

def x_increase(state):
    if state == 0:
        print('{}↔ Cam Stop!{}'.format(fg('magenta'), attr('reset')))
    elif state == 1:
        print('{}→ Cam Right!{}'.format(fg('magenta'), attr('reset')))
        action('x+')

def x_decrease(state):
    if state == 0:
        print('{}↔ Cam Stop!{}'.format(fg('magenta'), attr('reset')))
    elif state == 1:
        print('{}← Cam Left!{}'.format(fg('magenta'), attr('reset')))
        action('x-')

def y_increase(state):
    if state == 0:
        print('{}↕ Cam Stop!{}'.format(fg('cyan'), attr('reset')))
    elif state == 1:
        print('{}↑ Cam Up!{}'.format(fg('cyan'), attr('reset')))
        action('y+')

def y_decrease(state):
    if state == 0:
        print('{}↕ Cam Stop!{}'.format(fg('cyan'), attr('reset')))
    elif state == 1:
        print('{}↓ Cam Down!{}'.format(fg('cyan'), attr('reset')))
        action('y-')

def quit_fun(state):
    print('Quit!')
    action('stop')
    if connect_to_car:
	    tcpCliSock.close()

def reset(state):
    if state == 0:
        print('{}Cleared & Zeroed{}'.format(fg('red'), attr('reset')))
        action('speed100')
        action('home')
        action('xy_home')

def hello(state):
    if state == 0:
        print('{}Ready!{}'.format(fg('green'), attr('reset')))
    elif state == 1:
        print('{}Cam Home!{}'.format(fg('green'), attr('reset')))
        action('xy_home')

'''
Set which actions happen when buttons and joysticks change:
'''
event_lut = {
    'BTN_TOP2' : exit,          #LEFT_FINGER
    'BTN_BASE3' : reset,        #SELECT
    'BTN_BASE4' : hello,        #START
    'BTN_TOP' : x_decrease,     #GREEN(Y)
    'BTN_TRIGGER' : y_increase, #BLUE(X)
    'BTN_THUMB' : x_increase,   #RED(A)
    'BTN_THUMB2' : y_decrease,  #YELLOW(B)
    'ABS_X' : x,                #LEFT/RIGHT
    'ABS_Y' : y,                #UP/DOWN
}

def event_loop(events):
    '''
    This function is called in a loop, and will get the events from the
    controller and send them to the functions we specify in the `event_lut`
    dictionary
    '''
    for event in events:
        #print('\t', event.ev_type, event.code, event.state)
        call = event_lut.get(event.code)
        if callable(call):
           call(event.state)

if __name__ == '__main__':
    pads = inputs.devices.gamepads
    if len(pads) == 0:
        raise Exception("{}Couldn't find any Gamepads!{}".format(fg('red'), attr('reset')))
    reset(0)
    try:
        while True:
            event_loop(inputs.get_gamepad())
    except KeyboardInterrupt:
        print('Bye!')
        quit_fun(0)
    except:
        print('Byeee!!!')
        quit_fun(0)