from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from chatterbot.response_selection import get_first_response
from chatterbot.logic import BestMatch
from chatterbot.comparisons import Comparator
import json
import re
import spacy
from nltk.corpus import stopwords

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Load stopwords
stop_words = set(stopwords.words('english'))

def clean_input(text):

    text = re.sub(r'[^a-z0-9\s]', '', text.lower())
    doc = nlp(text)
    return ' '.join([token.lemma_ for token in doc if token.text not in stop_words])

class SpacySimilarity(Comparator):
    def compare(self, statement, other_statement):
        doc1 = nlp(statement.text)
        doc2 = nlp(other_statement.text)
        return doc1.similarity(doc2)

# Initialize the chatbot
chatbot = ChatBot(
    'GameBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'statement_comparison_function': SpacySimilarity(language='en'),
            'response_selection_method': get_first_response
        },
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter',
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': 'help',
            'output_text': 'I am here to assist you with your gaming questions!'
        }
    ],
    database_uri='sqlite:///gamebot_db.sqlite3'
)

# Load custom dataset
with open("game_dataset.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Train the chatbot with custom data
trainer = ListTrainer(chatbot)
for conversation in data:
    trainer.train([clean_input(msg) for msg in conversation])

# Train the chatbot with pre-trained corpora
corpus_trainer = ChatterBotCorpusTrainer(chatbot)
corpus_trainer.train(
    'chatterbot.corpus.english',
    'chatterbot.corpus.english.greetings',
    'chatterbot.corpus.english.conversations'
)

# Add context awareness (simple implementation)
context = {}

def get_response_with_context(user_input):
    global context
    cleaned_input = clean_input(user_input)
    response = chatbot.get_response(cleaned_input)

    # Update context
    context['last_user_input'] = user_input
    context['last_bot_response'] = response.text

    return response

# Example usage
if __name__ == "__main__":
    print("Bot: Hello! Ask me a question about video games.")
    while True:
        try:
            user_input = input("You: ")

            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("Bot: See you next time!")
                break

            response = get_response_with_context(user_input)
            print("Bot:", response)

        except (KeyboardInterrupt, EOFError, SystemExit):
            break
        except Exception as e:
            print("An error occurred:", str(e))
            break
