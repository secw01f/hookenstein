from flask import Flask, request, jsonify, abort
from importlib import import_module
from functools import wraps
import json
import jwt
import string
import random
import sys
import getopt

class Server:
    def __init__(self, port, module, auth, **kwargs):
        self.port = port
        self.module = import_module(f'modules.{module}')
        self.hook = self.module.Hook(**kwargs)
        self.auth = auth

        if self.auth == True:
            letters = string.ascii_lowercase
            self.key = (''.join(random.choice(letters) for i in range(50)))
            self.token = jwt.encode({"module": self.module.__name__}, self.key, algorithm='HS256')   

    def webserver(self):
        def auth_required(f):
            @wraps(f)
            def auth(*args, **kwargs):
                if self.auth == True:
                    token = request.headers['Authorization'].split()[1]
                    try:
                        jwt.decode(token, self.key, algorithms='HS256')
                        return f(*args, **kwargs)
                    except:
                        abort(403)
                elif self.auth == False:
                    return f(*args, **kwargs)
            return auth
        
        app = Flask(__name__)
        if self.auth == True:
            print(f'Authorization token: {self.token}\n')
   
        @app.route("/webhook", methods=["POST"])
        @auth_required
        def webhook():
            input = request.json
            self.hook.hook(input)
            response = {"response": "200"}
            return jsonify(response)
        
        @app.route("/status", methods=["GET"])
        def status():
            status = {"status": "200"}
            return jsonify(status)

        app.run(port=self.port, host='0.0.0.0')

if __name__ == '__main__':
    port = "8000"
    module = ""
    auth = False
    args = ""

    def usage():
        print('Hookenstein')
        print('')
        print('Modular Webhook Server')
        print('')
        print('Usage:')
        print('-h    --help      Shows this help message')
        print('-p    --port      Port number for the server to run (default: 8000)')
        print('-m    --module    Webhook module to use (required)')
        print('-a    --auth      Enable authentication requirement (default: Disabled)')
        print('-A    --args      Dictionary of arguments to pass to the module')
        print('')
        print('Example:')
        print('hookenstein.py -p 8000 -m example -a -A \'{"arg1": "value1", "arg2": "value2"}\'')

    if not sys.argv[1:]:
        usage()
        sys.exit()
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hp:m:aA:', ['help', 'port', 'module', 'auth', 'args'])
    except getopt.GetoptError as e:
        print(str(e))
        sys.exit()

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-p', '--port'):
            port = a
        elif o in ('-m', '--module'):
            module = a
        elif o in ('-a', '--auth'):
            auth = True
        elif o in ('-A', '--args'):
            args = json.loads(a)

    if module == "":
        print('A module is required')
        sys.exit()
    if len(args) != 0:
        print(f'Webhook server running on port {port} for module {module}...\n')
        webhook = Server(port, module, auth, **args)
        webhook.webserver()
    else:
        print(f'Webhook server running on port {port} for module {module}...\n')
        webhook = Server(port, module, auth)
        webhook.webserver()
