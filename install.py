import os
import requests
from configparser import ConfigParser

def check_config_file():
    config_file = 'config.ini'

    if not os.path.isfile(config_file):
        create_config_file(config_file)

    config = ConfigParser()
    config.read(config_file)

    if 'asterisk' not in config:
        config['asterisk'] = {}

    if 'server_address' not in config['asterisk']:
        server_address = input("Asterisk URL: ")
        config['asterisk']['server_address'] = server_address

    if 'server_protocol' not in config['asterisk']:
        server_protocol = input("Web Server Protocol (default https): ")
        if not server_protocol:
            server_protocol = 'https'
        config['asterisk']['server_protocol'] = server_protocol

    if 'ari_port' not in config['asterisk']:
        ari_port = input("ARI Port (default 8088): ")
        if not ari_port:
            ari_port = '8088'
        config['asterisk']['ari_port'] = ari_port

    if 'ari_username' not in config['asterisk']:
        ari_username = input("ARI User: ")
        config['asterisk']['ari_username'] = ari_username

    if 'ari_password' not in config['asterisk']:
        ari_password = input("ARI Password: ")
        config['asterisk']['ari_password'] = ari_password

    if 'telegram' not in config:
        config['telegram'] = {}

    if 'token' not in config['telegram']:
        token = input("Telegram Bot Token: ")
        config['telegram']['token'] = token

    if 'endpoint' not in config['telegram']:
        endpoint = input("Telegram Webhook Endpoint: ")
        config['telegram']['endpoint'] = endpoint

    with open(config_file, 'w') as file:
        config.write(file)

    set_endpoint(endpoint, token)
    replace_server_address(endpoint)
    print(f'\n\ncopy the code from extensions_custom.conf to the appropriate file on your PBX server {server_protocol}://{server_address}')

def create_config_file(config_file):
    config = ConfigParser()
    with open(config_file, 'w') as file:
        config.write(file)

def set_endpoint(endpoint, token):
    resp = requests.get(f'https://api.telegram.org/bot{token}/setWebhook?url={endpoint}/telegramisk')
    if resp.status_code == 200:
        hook_info = requests.get(f'https://api.telegram.org/bot{token}/getWebhookInfo').json()
        print('Webhook is already set', hook_info)
    else:
        print(resp.status_code, resp.json())


def replace_server_address(new_server_address):
    with open("extensions_custom.conf", 'r') as file:
        content = file.read()

    # Perform the replacement
    content = content.replace("<server_address>", new_server_address)

    with open("extensions_custom.conf", 'w') as file:
        file.write(content)


bot_token = check_config_file()