from flask import Flask, request
import  tlgrm

app = Flask(__name__)

@app.route('/telegramisk', methods=['POST'])
def tlgrm_receiver():
    tlgrm.tlgrm_processed()
    return "Webhook received!"

@app.route('/asterisk', methods=['POST'])
def aster_receiver():
    call_data = request.get_json()
    tlgrm.chat_ids_verified(call_data)

    return "Webhook received!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)