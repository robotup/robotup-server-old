# Robot Server v1.3 30.03.2019

import time, serial, string, time, os, random, hashlib, logging, argparse, re
from flask import *
import logging

# INITIALIZING SOME DEFINITIONS
ROBOT_VERSION = 'v1.3'

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
# PARSING
parser = argparse.ArgumentParser()
parser.add_argument("serial_port", help="serial port address where robot is connected to", type=str)
parser.add_argument("serial_freq", help="serial port frequency", type=str)
args = parser.parse_args()

# GENERATING TOKENS
def token_generate(length):
    letters = string.ascii_lowercase+string.digits
    return ''.join(random.choice(letters) for i in range(length))
real_token = token_generate(128)
webuser_username = 'robot'
webuser_password = token_generate(8)
real_token_text = '\n-- PASSWORD:   '+webuser_password+'\n'



#OUTPUT
print('\n   Welcome to the Robot server '+ROBOT_VERSION+'  \n '+real_token_text)

# WEB ERROR HANDLERS
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
@app.errorhandler(403)
def access_forbidden(e):
    return render_template('403.html'), 403
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# WEB INTERFACE 
@app.route('/')
@app.route('/index')
def index():
    
    if request.authorization and request.authorization.username == webuser_username and request.authorization.password == webuser_password: 
        token = {'token': real_token } 
        return render_template("index.html", token=token)
    return make_response('403 Forbidden', 401, {'WWW-Authenticate' : 'Basic realm="Login Required!"'})

# CONNECTING SERIAL
try:
    ser = serial.Serial(args.serial_port, args.serial_freq)
    time.sleep(3)
    print('   Successfully connected to <{0}> !\n'.format(args.serial_port))
except Exception:
    print('== Error: Could not connect to <{0}> !\n'.format(args.serial_port))

def no_conn_exeption():
    print('== Error: No device connected!')

# MOVING ROBOT
def stop(event):
    try:
        ser.write(b's')
    except:
        no_conn_exeption()

def move_left(event):
    try:
        ser.write(b'l')
        print("-- Moving Left!")
    except:
        no_conn_exeption()

def move_right(event):
    try:
        ser.write(b'r')
        print("-- Moving Right!")
    except:
        no_conn_exeption()

def move_forward(event):
    try:
        ser.write(b'f')
        print("-- Moving Forward!")
    except:
        no_conn_exeption()

def move_backward(event):
    try:
        ser.write(b'b')
        print("-- Moving Backward!")
    except:
        no_conn_exeption()

# WEB INTERFACE AGAING
@app.route('/control', methods = ['GET'])
def moving():
    global real_token
    token = request.args.get('token')
    move = request.args.get('move')
    lights = request.args.get('lights')
    if(token == real_token):
## WEB MOVING
        if(move == 'l'):
            try:
                ser.write(b'l')
                print('-- LEFT') 
                data = {'move' : 'left'}
            except:        
                print('== Cannot move! Please check connection.')    
                data = {'error' : '2'}
        elif(move == 'r'):
            try:
                ser.write(b'r')
                print('-- RIGHT') 
                data = {'move' : 'right'}
            except:        
                print('== Cannot move! Please check connection.')    
                data = {'error' : '2'} 
        elif(move == 'f'):
            try:
                ser.write(b'f')
                print('-- FORWARD') 
                data = {'move' : 'forward'}
            except:        
                print('== Cannot move! Please check connection.')    
                data = {'error' : '2'}
        elif(move == 'b'):
            try:
                ser.write(b'b')
                print('-- BACK') 
                data = {'move' : 'back'}
            except:        
                print('== Cannot move! Please check connection.')    
                data = {'error' : '2'}
        elif(move == 's'):
            try:
                ser.write(b's')
                print('-- STOP') 
                data = {'move' : 'left'}
            except:        
                print('== Cannot move! Please check connection.')    
                data = {'error' : '2'}  
        ## LIGHTS
        elif(lights == '1'):
            try:
                ser.write(b'e')
                print('-- LTS ON') 
                data = {'lights' : '1'}
            except:        
                print('== Cannot toggle lights! Please check connection.')    
                data = {'error' : '2'}  
        elif(lights == '0'):
            try:
                ser.write(b'r')
                print('-- LTS OFF') 
                data = {'lights' : '0'}
            except:        
                print('== Cannot toggle lights! Please check connection.')    
                data = {'error' : '2'} 
        else:
            data = {'error' : '1'}
    else:
        abort(404)

    js = json.dumps(data)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

# RUNNING APP
if __name__ == "__main__":
    app.run('0.0.0.0', port='8080')
