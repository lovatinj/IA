
import re

def remove_french_stopwords(input_text):
    stop_file = open("SVM_avec_traitement/stopwords.txt","r")
    stop_list = []
    for ligne in stop_file:
        stop_list.append(ligne[:-1])
    stop_file.close()

    # Tokenisation des mots
    words = re.findall(r'\b\w+\b', str(input_text))

    # Suppression des stopwords
    filtered_words = []
    for mot in words:
        if mot.lower() not in stop_list:
            filtered_words.append(mot)

    # Reconstruction de la chaîne de caractères sans les stopwords
    output_text = ' '.join(filtered_words)

    return str(output_text)
