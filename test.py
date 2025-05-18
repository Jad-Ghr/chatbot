from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot import ChatBot

chatbot = ChatBot(
    'MyBot',
    logic_adapters=[
        'chatterbot.logic.BestMatch'
    ]
)

# Train the chatbot with some English corpus data
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train('chatterbot.corpus.english')

# Simple chat loop
while True:
    try:
        user_input = input("You: ")
        response = chatbot.get_response(user_input)
        print("Bot:", response)
    except (KeyboardInterrupt, EOFError):
        print("\nExiting.")
        break
