import tensorflow as tf
import numpy as np
import pickle
import json
from tensorflow.keras.preprocessing.sequence import pad_sequences


# Load the dataset for answer mapping
with open('dataset.json', 'r') as file:
    data = json.load(file)

# Load the trained model
model = tf.keras.models.load_model("final_model.h5")

# Load the tokenizer used during training
with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

# Set the same sequence length used in training
MAX_SEQUENCE_LENGTH = 46
START_TOKEN = tokenizer.word_index.get("<start>", 1)  # Replace with actual start token index
END_TOKEN = tokenizer.word_index.get("<end>", 2)  # Replace with actual end token index

# Map predicted class to answers
answer_list = []
for game in data['games']:
    for level in game['levels']:
        strategy = level['strategy']
        if strategy not in answer_list:
            answer_list.append(strategy)

answer_map = {i: strategy for i, strategy in enumerate(answer_list)}

def predict_answer(user_input, beam_width=3):
    # Tokenize and pad the user input
    sequence = tokenizer.texts_to_sequences([user_input])
    padded_input = pad_sequences(sequence, maxlen=MAX_SEQUENCE_LENGTH, padding='post')
    print("DEBUG: Tokenized input:", sequence)
    print("DEBUG: Padded input:", padded_input)

    # Initialize decoder input with the start token
    decoder_input = np.zeros((1, 1))
    decoder_input[0, 0] = START_TOKEN

    # Beam search variables
    sequences = [[[], 0]]  # List of [sequence, score]

    for _ in range(MAX_SEQUENCE_LENGTH):
        all_candidates = []
        for seq, score in sequences:
            # Update decoder input with the current sequence
            decoder_input = np.zeros((1, len(seq) + 1))
            decoder_input[0, :] = [START_TOKEN] + seq

            # Predict next token probabilities
            predictions = model.predict([padded_input, decoder_input])
            token_probs = predictions[0, -1, :]  # Get probabilities for the last token

            # Expand each candidate
            for token_idx, prob in enumerate(token_probs):
                candidate = [seq + [token_idx], score - np.log(prob + 1e-9)]  # Add log probability
                all_candidates.append(candidate)

        # Select top-k candidates
        sequences = sorted(all_candidates, key=lambda x: x[1])[:beam_width]

    # Select the best sequence
    best_sequence = sequences[0][0]

    # Convert predicted indices to text
    predicted_text = " ".join(
        [tokenizer.index_word.get(idx, "") for idx in best_sequence if idx != END_TOKEN]
    )

    print("DEBUG: Predicted indices:", best_sequence)
    print("DEBUG: Predicted text:", predicted_text)

    return predicted_text or "Sorry, I didn't understand." 


# # Example input
# question = "Inside the Deku Tree Your first dungeon inside the guardian spirit of the Kokiri Forest. You must navigate through its hollowed interior, solving puzzles and defeating enemies. Destroy the parasitic curse inside the Deku Tree by defeating Queen Gohma."
# print("User:", question)
# print("Chatbot:", predict_answer(question))