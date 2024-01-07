import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Bidirectional, LSTM, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import xml.etree.ElementTree as ET
import tensorflow as tf
from tensorflow.keras.layers import Embedding, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.regularizers import l2
from tensorflow.keras.callbacks import EarlyStopping

# Charger le fichier XML
def xmltodata(fichier_xml):
    data = []
    tree = ET.parse(fichier_xml)
    root = tree.getroot()
    for critique in root.findall('comment'):
        film = critique.find('movie').text
        user_id = critique.find('user_id').text
        note = critique.find('note').text
        commentaire = critique.find('commentaire').text
        if commentaire is None:
            commentaire = ""
        data.append([film, user_id, note, commentaire])
    return data

def xmltodata_test(fichier_xml):
    data = []
    tree = ET.parse(fichier_xml)
    root = tree.getroot()
    for critique in root.findall('comment'):
        film = critique.find('movie').text
        user_id = critique.find('user_id').text
        commentaire = critique.find('commentaire').text
        if commentaire is None:
            commentaire = ""
        data.append([film, user_id, commentaire])
    return data

def review(fichier_xml):
    data = []
    tree = ET.parse(fichier_xml)
    root = tree.getroot()
    for critique in root.findall('comment'):
        review = critique.find('review_id').text
        data.append(review)
    return data

# Chargement des données...
print("Chargement des données ...")
data_train = xmltodata("drive/MyDrive/Colab_Notebooks/train.xml")
data_dev = xmltodata("drive/MyDrive/Colab_Notebooks/dev.xml")
data_test = xmltodata_test("drive/MyDrive/Colab_Notebooks/test.xml")

train_messages = []
train_labels = []
dev_messages = []
dev_labels = []
test_messages = []

for critique in data_train:
    train_messages.append(critique[3])
    train_labels.append(float(critique[2].replace(',', '.')))
for critique in data_dev:
    dev_messages.append(critique[3])
    dev_labels.append(float(critique[2].replace(',', '.')))
for critique in data_test:
    test_messages.append(critique[2])

print("Fin du chargement des données" + "\n")

# Prétraitement des données...
print("Prétraitement des données ...")
tokenizer = Tokenizer()
tokenizer.fit_on_texts(train_messages + dev_messages)

train_sequences = tokenizer.texts_to_sequences(train_messages)
dev_sequences = tokenizer.texts_to_sequences(dev_messages)
test_sequences = tokenizer.texts_to_sequences(test_messages)

vocab_size = len(tokenizer.word_index) + 1

max_len = 100
train_padded = pad_sequences(train_sequences, maxlen=max_len, padding='post')
dev_padded = pad_sequences(dev_sequences, maxlen=max_len, padding='post')
test_padded = pad_sequences(test_sequences, maxlen=max_len, padding='post')

# Création du modèle avec une couche Bidirectional LSTM
print("Génération du modèle avec une couche Bidirectional LSTM ...")
model = Sequential()
model.add(Embedding(input_dim=vocab_size, output_dim=50, input_length=max_len))
model.add(Bidirectional(LSTM(100, return_sequences=True)))
model.add(Bidirectional(LSTM(100)))
model.add(Flatten())
model.add(Dense(256, activation='relu', kernel_regularizer=l2(0.01)))
model.add(BatchNormalization())
model.add(Dropout(0.2))
model.add(Dense(256, activation='relu', kernel_regularizer=l2(0.01)))
model.add(BatchNormalization())
model.add(Dropout(0.2))
model.add(Dense(1, activation='linear'))
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

# Entraînement du modèle...
print("Entraînement du modèle ...")
model.fit(np.array(train_padded), np.array(train_labels), epochs=5, validation_data=(np.array(dev_padded), np.array(dev_labels)))

# Évaluation du modèle sur le jeu de test
test_predictions = model.predict(test_padded)

# Affichage
print("Évaluation du modèle sur le jeu de test ...")
data_review = review("drive/MyDrive/Colab_Notebooks/test.xml")

with open("out_bidirectional_lstm.txt", 'w') as file:
    for prediction in test_predictions:
        file.write(f"{prediction[0]}\n")

print("Fin du programme !")
