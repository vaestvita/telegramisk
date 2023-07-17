import requests
import threading
import time
import random
import string
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')
pbxurl = config.get('asterisk', 'server_address')
pbxport = config.get('asterisk', 'ari_port')
server_protocol = config.get('asterisk', 'server_protocol')
ari_username = config.get('asterisk', 'ari_username')
ari_password = config.get('asterisk', 'ari_password')


def find_number(number, code=None):
    endpoints = requests.get(f'{server_protocol}://{pbxurl}:{pbxport}/ari/endpoints', 
                               auth=(ari_username, ari_password)).json()

    number_data = {'message': None, 'code': None, 'found': False}

    for endpoint in endpoints:
        if endpoint['resource'] == str(number):
            if endpoint['state'] == 'online':
                number_data['found'] = True
                number_data['message'] = f'Extension {number} found. Wait for a call with a code. Send {number}#<code> to confirm'
                technology = endpoint['technology']
                if not code:
                    code = generate_verification_code()
                    number_data['code'] = code
                threading.Thread(target=verify_call, args=(number, code, technology)).start()
            else:
                number_data['found'] = True
                number_data['message'] = f'Extension {number} found, but not online. Register it and try again.'

    if not number_data['found']:
        number_data['message'] = f'Extension {number} not found.'

    return number_data           
      

def verify_call(number, code, technology):
    
    payload = {
        'endpoint': f'{technology}/{number}',
        'extension': 's',
        'context': 'verify_number',
        'priority': 1,
        'timeout': 30,
        'callerId': 'telegramisk',
        'variables': {
            'verification_code': f'{code}'
        }
    }

    time.sleep(5)

    requests.post(f'{server_protocol}://{pbxurl}:{pbxport}/ari/channels', 
                                 auth=(ari_username, ari_password), json=payload)
    

def generate_verification_code():
    code = ''.join(random.choices(string.digits, k=4))
    return code   