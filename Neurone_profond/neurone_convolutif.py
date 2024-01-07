import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Conv1D, GlobalMaxPooling1D, Dense, Dropout, BatchNormalization
from tensorflow.keras.regularizers import l2
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import EarlyStopping
import xml.etree.ElementTree as ET
from tensorflow.keras.utils import plot_model

# Charger le fichier xml

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

def remove_stopwords(text, stopwords):
    # Retirer les mots présents dans la liste de stopwords
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stopwords]
    return ' '.join(filtered_words)

print("Chargement des données ...")
#Chargement des jeux de données train, dev et test.
data_train = xmltodata("drive/MyDrive/Colab_Notebooks/train.xml")
data_dev = xmltodata("drive/MyDrive/Colab_Notebooks/dev.xml")
data_test = xmltodata_test("drive/MyDrive/Colab_Notebooks/test.xml")

# Charger la liste des stopwords depuis le fichier
with open("drive/MyDrive/Colab_Notebooks/stopwords.txt", "r", encoding="utf-8") as stopword_file:
    stopwords = stopword_file.read().splitlines()

train_messages = []
train_labels = []
dev_messages = []
dev_labels = []
test_messages = []

# Modifier les commentaires en retirant les stopwords
for critique in data_train:
    cleaned_comment = remove_stopwords(critique[3], stopwords)
    train_messages.append(cleaned_comment)
    train_labels.append(float(critique[2].replace(',', '.')))

for critique in data_dev:
    cleaned_comment = remove_stopwords(critique[3], stopwords)
    dev_messages.append(cleaned_comment)
    dev_labels.append(float(critique[2].replace(',', '.')))

for critique in data_test:
    cleaned_comment = remove_stopwords(critique[2], stopwords)
    test_messages.append(cleaned_comment)

print("Fin du chargement des données" + "\n")

print("Prétraitement des données ...")

tokenizer = Tokenizer()
tokenizer.fit_on_texts(train_messages)

train_sequences = tokenizer.texts_to_sequences(train_messages)
dev_sequences = tokenizer.texts_to_sequences(dev_messages)
test_sequences = tokenizer.texts_to_sequences(test_messages)

vocab_size = len(tokenizer.word_index) + 1

max_len = 100
train_padded = pad_sequences(train_sequences, maxlen=max_len, padding='post')
dev_padded = pad_sequences(dev_sequences, maxlen=max_len, padding='post')
test_padded = pad_sequences(test_sequences, maxlen=max_len, padding='post')
print("Fin du prétraitement des données ..." + "\n")

print("Génération du modèle ...")

model = Sequential()
model.add(Embedding(input_dim=vocab_size, output_dim=50, input_length=max_len))
model.add(Conv1D(128, 5, activation='relu'))
model.add(GlobalMaxPooling1D())
model.add(Dense(256, activation='relu', kernel_regularizer=l2(0.01)))
model.add(Dense(256, activation='relu', kernel_regularizer=l2(0.01)))
model.add(Dense(1, activation='linear'))

model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

model.fit(
    np.array(train_padded),
    np.array(train_labels),
    epochs=10,
    validation_data=(np.array(dev_padded), np.array(dev_labels)),
    # callbacks=[early_stopping]
)

test_predictions = model.predict(test_padded)

data_review = review("drive/MyDrive/Colab_Notebooks/test.xml")

with open("out_cnn.txt", 'w') as file:
    for prediction in test_predictions:
        file.write(f"{prediction[0]}\n")

print("Fin du programme !")
