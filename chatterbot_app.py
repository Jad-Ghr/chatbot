from flask import Flask, request, jsonify
from flask_cors import CORS
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatbotsimple import les_reponses
from appfun import predict_answer  
import json
import os

app = Flask(__name__)
CORS(app)

# Initialize the chatbot
chatbot = ChatBot('GameBot', database_uri='sqlite:///gamebot_db.sqlite3')

# Train the chatbot only if the database is empty
if not os.path.exists("gamebot_db.sqlite3") or os.stat("gamebot_db.sqlite3").st_size == 0:
    trainer = ListTrainer(chatbot)
    try:
        with open("game_dataset.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            for conversation in data:
                if isinstance(conversation, list):
                    trainer.train(conversation)
        else:
            print("Invalid dataset format. Expected a list of conversations.")
    except FileNotFoundError:
        print("Error: game_dataset.json not found.")
    except Exception as e:
        print(f"An error occurred while training the chatbot: {e}")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        user_input = request.json.get('message', '')
        model = request.json.get('model', 'chatterbot')  # Default to chatterbot if not provided
        if not user_input:
            return jsonify({'error': 'No input provided'}), 400

        # Choose model based on frontend selection
        if model == 'nltk':
            response = les_reponses(user_input)
        elif model == 'tensorflow':
            response = predict_answer(user_input)
        else:  # chatterbot
            response = chatbot.get_response(user_input)

        return jsonify({'answer': str(response)})
    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500
if __name__ == '__main__':
    app.run(debug=True)
