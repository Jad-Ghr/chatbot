import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, LSTM, Dense,Attention, Concatenate
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np     
import json
import pickle



# Load the file
with open('dataset.json', 'r') as file:
    data = json.load(file)


# Data Preprocessing
inputs = []
outputs = []

for game in data.get('games', []):
    for level in game.get('levels', []):
        try:
            # Concatenate title, description, and objective for the input
            input_text = f"{level['title']}  {level['description']} {level['objective']}"
            output_text = level['strategy']
            inputs.append(input_text)
            outputs.append(output_text)
        except KeyError as e:
            print(f"Missing key in level data: {e}")

# Initialize Tokenizer
tokenizer = Tokenizer(num_words=1000, oov_token="<OOV>")#.,;
tokenizer.fit_on_texts(inputs + outputs)

# Create sequences for inputs and outputs
input_sequences = tokenizer.texts_to_sequences(inputs)
output_sequences = tokenizer.texts_to_sequences(outputs)

# Pad sequences
max_input_len = max(len(seq) for seq in input_sequences)
max_output_len = max(len(seq) for seq in output_sequences)# {[8,3,5] [12,5] [2,5,9,1]}

input_pad = pad_sequences(input_sequences, maxlen=max_input_len, padding='post')
output_pad = pad_sequences(output_sequences, maxlen=max_output_len, padding='post')# {[8,3,5,0] [12,5,0,0] [2,5,9,1]}

# Create target data (shifted output_pad)
decoder_target_data = np.zeros_like(output_pad)
decoder_target_data[:, :-1] = output_pad[:, 1:]# {[3,5,0,0] [5,0,0,0] [2,5,9,1]}

# Split the data
x_train_enc, x_val_enc, x_train_dec, x_val_dec, y_train, y_val = train_test_split(
    input_pad, output_pad, decoder_target_data, test_size=0.2
)

# Hyperparameters
embedding_dim = 128
lstm_units = 256
vocab_size = len(tokenizer.word_index) + 1  # Add 1 for padding/OOV

# Build Model

def build_model():
    
    # Encoder
    encoder_inputs = Input(shape=(max_input_len,))
    encoder_embedding = Embedding(vocab_size, embedding_dim)(encoder_inputs)
    encoder_lstm = LSTM(lstm_units, return_state=True, return_sequences=True)
    encoder_outputs, state_h, state_c = encoder_lstm(encoder_embedding)

    # Decoder
    decoder_inputs = Input(shape=(max_output_len,))
    decoder_embedding = Embedding(vocab_size, embedding_dim)(decoder_inputs)
    decoder_lstm = LSTM(lstm_units, return_sequences=True, return_state=True)
    decoder_outputs, _, _ = decoder_lstm(decoder_embedding, initial_state=[state_h, state_c])

    # Reshape encoder outputs to match decoder outputs
    # Attention expects both inputs to have the same shape
    attention = Attention()([decoder_outputs, encoder_outputs])
    decoder_combined_context = Concatenate(axis=-1)([decoder_outputs, attention])

    # Dense Output Layer
    decoder_outputs = Dense(vocab_size, activation='softmax')(decoder_combined_context)

    # Define Model
    model = Model([encoder_inputs, decoder_inputs], decoder_outputs)
    return model

model = build_model()
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.summary()

# Add Callbacks
callbacks = [
    tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True),
    tf.keras.callbacks.ModelCheckpoint('best_model.h5', save_best_only=True)
]

# Train Model
history = model.fit(
    [x_train_enc, x_train_dec],
    y_train,
    validation_data=([x_val_enc, x_val_dec], y_val),
    batch_size=32,
    epochs=250,
    callbacks=callbacks
)

# Plot loss
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Val Loss')
plt.title('Loss Over Time')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

# Plot accuracy (if available)
if 'accuracy' in history.history:
    plt.subplot(1, 2, 2)
    plt.plot(history.history['accuracy'], label='Train Accuracy')
    plt.plot(history.history['val_accuracy'], label='Val Accuracy')
    plt.title('Accuracy Over Time')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()

plt.tight_layout()
plt.show()

# Save Tokenizer and Model
with open('tokenizer.pkl', 'wb') as f:
    pickle.dump(tokenizer, f)

model.save("final_model.h5")


