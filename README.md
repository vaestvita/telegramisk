**Project Description: Telegram Asterisk Integration (Telegramisk)**

This project provides an integration between the Telegram messaging platform and the Asterisk PBX system. It allows users to manage and verify their extension numbers through Telegram.

**Features:**
- User Registration: Users can register their Telegram account to link it with their extension number.
- Extension Verification: Users can verify their extension number by receiving a call with a verification code.
- List Numbers: Users can view a list of their linked extension numbers along with their verification status.
- Delete Number: Users can delete a linked extension number from their account.
- Verification Code Confirmation: Users can confirm the verification code received during the verification process.

**Project Structure:**

1. `tlgrm_processed()` function: This function serves as the main entry point for processing Telegram messages. It handles various commands and interacts with the user based on the received message.

2. `send_message(chat_id, message)` function: This function sends a message to a specific chat ID using the Telegram Bot API.

3. `chat_ids_verified(call_data)` function: This function retrieves the chat IDs of users whose extension numbers have been verified. It receives call data as input and sends a message to the verified users.

4. `find_number(number, code=None)` function: This function searches for an extension number in the Asterisk PBX system. It returns information about the number's availability and generates a verification code if needed.

5. `verify_call(number, code, technology)` function: This function initiates a call to the specified extension number for verification purposes. It uses the Asterisk ARI (Asterisk REST Interface) to create a channel and connect the call.

6. `generate_verification_code()` function: This function generates a random verification code consisting of four digits.

**Usage:**

To use this project, follow these steps:
1. Deploy the code on a server with access to the Asterisk PBX system.
2. Create a Telegram Bot and obtain the Bot Token.
3. Configure the Asterisk server address, ARI credentials, and other necessary parameters in the code.
4. Run the code, ensuring it is accessible via a public URL (e.g., using a reverse proxy or ngrok).
5. Set up a webhook to receive incoming messages and events from Telegram, directing them to the deployed code.
6. Users can interact with the Telegram Bot to register, verify extension numbers, view their linked numbers, and perform other supported actions.

**Note:** This project assumes the availability of an Asterisk PBX system and requires proper configuration of the server, ARI, and other related components.

**Quick Setup Process using install.py**

To quickly set up the configuration file for the project, follow these steps by running the `install.py` file:

1. Execute the `install.py` file. It will check if the `config.ini` file exists. If not, it will create it.

2. Enter the following Asterisk-related configuration details prompted by the script:
   - Asterisk URL: Enter the URL of your Asterisk server.
   - Web Server Protocol (default: https): Optionally specify the protocol for the web server.
   - ARI Port (default: 8088): Optionally specify the port for the Asterisk REST Interface (ARI).
   - ARI User: Enter the username for ARI authentication.
   - ARI Password: Enter the password for ARI authentication.

3. Enter the following Telegram-related configuration details prompted by the script:
   - Telegram Bot Token: Enter the token for your Telegram Bot.
   - Telegram Webhook Endpoint: Enter the webhook endpoint where the Telegram events will be received.

4. The configuration file (`config.ini`) will be updated with the entered values.

5. The script will set the webhook for the Telegram Bot using the provided endpoint. It will verify if the webhook is already set and display the webhook information if applicable.

6. The script will replace the `<server_address>` placeholder in the `extensions_custom.conf` file with the new server address provided.

7. Finally, a message will be displayed, instructing you to copy the code from the `extensions_custom.conf` file and place it in the appropriate file on your PBX server. The message will also show the server address and protocol.

By following these steps, you can quickly configure the project by providing the necessary Asterisk and Telegram details, set up the webhook, and replace the server address in the required configuration file.