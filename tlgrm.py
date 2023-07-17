import json
import os
import requests

from flask import request
from configparser import ConfigParser
from aster import find_number

config = ConfigParser()
config.read('config.ini')
bot_token = config.get('telegram', 'token')

def open_users_file():
    with open('users.json', 'r') as file:
        users = json.load(file)
        return users

def tlgrm_processed():
    file_path = 'users.json'
    if not os.path.isfile(file_path):
        with open(file_path, 'w') as file:
            json.dump([], file)

    users = open_users_file()
    
    event = request.get_json()
    print(event)
    message_text = event['message']['text']
    chat_id = event['message']['chat']['id']
    found_user = False

    if message_text == "/start":
        existing_user = next((user for user in users if user['chat_id'] == chat_id), None)
        if existing_user is None:
            users.append({'chat_id': chat_id, 'numbers': [], 'username': event['message']['chat']['username']})
            with open('users.json', 'w') as file:
                json.dump(users, file, indent=4)
            send_message(chat_id, 'User added')
        else:
            send_message(chat_id, 'User already exists')
        return 'OK'
    
    else:    
        for user in users:
            if user['chat_id'] == chat_id:
                found_user = True
                if message_text == "/set_number":
                    send_message(chat_id, 'Extension Number:')
                    return 'OK'

                elif message_text.isdigit():
                    number = int(message_text)

                    if any(number == n['number'] for n in user['numbers']):
                        for n in user['numbers']:
                            if number == n['number']:
                                if n['status'] == 'verified':
                                    send_message(chat_id, f'{number} already verified')
                                else:
                                    send_message(chat_id, find_number(number, n['status'])['message'])
                    else:
                        number_state = find_number(number)
                        code = number_state['code']
                        message = number_state['message']
                        if code:
                            user['numbers'].append({"number": number, "status": code})
                            with open('users.json', 'w') as file:
                                json.dump(users, file, indent=4)
                        send_message(chat_id, message)

                elif message_text == "/list_numbers":
                    numbers = user['numbers']
                    if numbers:
                        numbers_text = '\n'.join(f"Ext: {number['number']}, Status: {'Verified' if number['status'] == 'verified' else 'Not verified'}" for number in numbers)
                        send_message(chat_id, f'Extensions:\n{numbers_text}\n\nTo delete, enter: del <num>\nEnter the number again to verify.')
                    else:
                        send_message(chat_id, 'No Extensions')

                elif '#' in message_text:
                    num, code = message_text.split('#', 1)
                    num = int(num)
                    for number in user['numbers']:
                        if number['number'] == num:
                            if number['status'] == code:
                                number['status'] = 'verified'
                                with open('users.json', 'w') as file:
                                    json.dump(users, file, indent=4)
                                send_message(chat_id, f'{num} verified')
                            else:
                                send_message(chat_id, 'Incorrect Verification Code')
                            return 'OK'
                    send_message(chat_id, 'Extensions Not Found')
                    return 'OK'

                elif message_text.lower().startswith("del "):
                    number_to_delete = message_text.split(' ', 1)[1]
                    if number_to_delete.isdigit():
                        number_to_delete = int(number_to_delete)
                        for number in user['numbers']:
                            if number['number'] == number_to_delete:
                                user['numbers'].remove(number)
                                with open('users.json', 'w') as file:
                                    json.dump(users, file, indent=4)
                                send_message(chat_id, f'Ext {number_to_delete} deleted')
                                return 'OK'
                        send_message(chat_id, f'Extension {number_to_delete} is not linked to your account')
                    return 'OK'
                
                else:
                    send_message(chat_id, 'Unknown command')
                    return 'OK'

        if not found_user:
            send_message(chat_id, 'User not found')
            return 'OK'
    return 'ok'


def send_message(chat_id, message):
    send_message_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(send_message_url, json=payload)
    return response.json()


def chat_ids_verified(call_data):
    print(call_data)
    number = int(call_data['ext'])
    users = open_users_file()
    verified_chat_ids = []
    for entry in users:
        for num in entry["numbers"]:
            if num["number"] == number and num["status"] == "verified":
                verified_chat_ids.append(entry["chat_id"])
                break
    if verified_chat_ids:
        message = f"{call_data['phone']} {call_data['Status']}"
        for chat_id in verified_chat_ids:
            send_message(chat_id, message)