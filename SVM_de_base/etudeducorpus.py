import xmltodata
import matplotlib.pyplot as plt
import numpy as np
import random
from collections import Counter
import re

data_train = xmltodata.xmltodata("donnees_appr_dev/donnees_appr_dev/train.xml")
data_dev = xmltodata.xmltodata("donnees_appr_dev/donnees_appr_dev/dev.xml")

def histogramme_note_globale():
    dico_note_train = {"0,5":0 ,"1,0":0,"1,5":0,"2,0":0,"2,5":0,"3,0":0,"3,5":0,"4,0":0,"4,5":0,"5,0":0}
    dico_note_dev = {"0,5":0 ,"1,0":0,"1,5":0,"2,0":0,"2,5":0,"3,0":0,"3,5":0,"4,0":0,"4,5":0,"5,0":0}
    nb_notes_train = 0
    nb_notes_dev = 0

    for critique_train in data_train:
        dico_note_train[critique_train[2]] += 1
        nb_notes_train += 1

    for critique_dev in data_dev:
        dico_note_dev[critique_dev[2]] += 1
        nb_notes_dev += 1

    #Calcul des moyennes 
    moyenne_train = 0
    moyenne_dev = 0
    for note in dico_note_train.keys():
        moyenne_train += float(note.replace(',', '.')) * dico_note_train[note]
    moyenne_train /= nb_notes_train
    for note in dico_note_dev.keys():
        moyenne_dev += float(note.replace(',', '.')) * dico_note_dev[note]
    moyenne_dev /= nb_notes_dev
    
    # Les catégories (niveaux de notes)
    categories = list(dico_note_train.keys())

    # Les fréquences associées à chaque catégorie
    valeurs_train = [(valeur / nb_notes_train)*100 for valeur in list(dico_note_train.values())]
    valeurs_dev = [(valeur / nb_notes_dev)*100 for valeur in list(dico_note_dev.values())]

    # Créer un histogramme
    largeur_barre = 0.35  # Largeur des barres
    indices = np.arange(len(categories))  # Indices pour les catégories

    plt.bar(indices, valeurs_train, width=largeur_barre, color='skyblue', label='Train')
    plt.bar(indices + largeur_barre, valeurs_dev, width=largeur_barre, color='purple', label='Dev')

    # Personnalisation de l'histogramme
    plt.title("Distributions des notes")
    plt.xlabel("Notes")
    plt.ylabel("Fréquence")
    plt.xticks(indices + largeur_barre / 2, categories, rotation=45)  # Ajuster les étiquettes d'axe x
    plt.legend()  # Afficher la légende

    # Afficher l'histogramme
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

def note_moyenne_film():
    dico_moyenne_film_train = {}
    dico_moyenne_train = {}
    dico_moyenne_film_dev = {}
    dico_moyenne_dev = {}


    for critique_train in data_train :
        if critique_train[0] not in dico_moyenne_film_train.keys():
            dico_moyenne_film_train[critique_train[0]] = [float(critique_train[2].replace(',', '.')),1]
        else :
            dico_moyenne_film_train[critique_train[0]][0] += float(critique_train[2].replace(',', '.'))
            dico_moyenne_film_train[critique_train[0]][1] += 1

    for critique_dev in data_dev :
        if critique_dev[0] not in dico_moyenne_film_dev.keys():
            dico_moyenne_film_dev[critique_dev[0]] = [float(critique_dev[2].replace(',', '.')),1]
        else :
            dico_moyenne_film_dev[critique_dev[0]][0] += float(critique_dev[2].replace(',', '.'))
            dico_moyenne_film_dev[critique_dev[0]][1] += 1


    for film in dico_moyenne_film_train.keys():
        dico_moyenne_train[film] = dico_moyenne_film_train[film][0] / dico_moyenne_film_train[film][1]

    for film in dico_moyenne_film_dev.keys():
        dico_moyenne_dev[film] = dico_moyenne_film_dev[film][0] / dico_moyenne_film_dev[film][1]  

    # Choisir 200 films au hasard
    nombre_de_films = 50
    films_aleatoires_train = random.sample(list(dico_moyenne_train.keys()), nombre_de_films)
    films_aleatoires_dev = random.sample(list(dico_moyenne_dev.keys()), nombre_de_films)

    # Obtenir les notes de ces films
    notes_aleatoires_train = [dico_moyenne_train[film] for film in films_aleatoires_train]
    notes_aleatoires_dev = [dico_moyenne_dev[film] for film in films_aleatoires_dev]
    
    # Calculer la moyenne des notes aléatoires
    moyenne_des_notes_train = sum(notes_aleatoires_train) / nombre_de_films
    moyenne_des_notes_dev = sum(notes_aleatoires_dev) / nombre_de_films

    # Créer un histogramme
    plt.figure(figsize=(10, 6))
    plt.bar(films_aleatoires_train, notes_aleatoires_train, color='skyblue',label="Train")
    plt.bar(films_aleatoires_dev, notes_aleatoires_dev, color='purple',label="Dev")
    plt.axhline(y=moyenne_des_notes_train, color='blue', linestyle='--', label='Moyenne Train')
    plt.axhline(y=moyenne_des_notes_dev, color='pink', linestyle='--', label='Moyenne Dev')
    plt.title("Notes de " + str(nombre_de_films) + " films choisi aléatoirement")
    plt.xlabel("Films")
    plt.ylabel("Notes")
    plt.xticks([],rotation=45)  # Ajuster les étiquettes d'axe x
    plt.legend()
    plt.tight_layout()

    # Afficher le graphique
    plt.show()

def boite_a_moustache():
    dico_note_train = {"0,5":0 ,"1,0":0,"1,5":0,"2,0":0,"2,5":0,"3,0":0,"3,5":0,"4,0":0,"4,5":0,"5,0":0}
    dico_note_dev = {"0,5":0 ,"1,0":0,"1,5":0,"2,0":0,"2,5":0,"3,0":0,"3,5":0,"4,0":0,"4,5":0,"5,0":0}
    nb_notes_train = 0
    nb_notes_dev = 0

    for critique_train in data_train:
        dico_note_train[critique_train[2]] += 1
        nb_notes_train += 1

    for critique_dev in data_dev:
        dico_note_dev[critique_dev[2]] += 1
        nb_notes_dev += 1

    #Calcul des moyennes 
    moyenne_train = 0
    moyenne_dev = 0
    for note in dico_note_train.keys():
        moyenne_train += float(note.replace(',', '.')) * dico_note_train[note]
    moyenne_train /= nb_notes_train
    for note in dico_note_dev.keys():
        moyenne_dev += float(note.replace(',', '.')) * dico_note_dev[note]
    moyenne_dev /= nb_notes_dev

    # Conversion des dictionnaires en listes
    liste_train = []
    for note, freq in dico_note_train.items():
        liste_train.extend([float(note.replace(',', '.'))] * freq)

    liste_dev = []
    for note, freq in dico_note_dev.items():
        liste_dev.extend([float(note.replace(',', '.'))] * freq)

    
    # Création des boîtes à moustaches
    plt.figure(1)
    plt.boxplot(liste_train, labels=['Train'])
    plt.title("Boîte à moustache sur le jeu Train")
    plt.ylabel("Notes")
    plt.grid(True)

    plt.figure(2)
    plt.boxplot(liste_dev, labels=['Dev'])
    plt.title("Boîte à moustache sur le jeu Dev")
    plt.ylabel("Notes")
    plt.grid(True)


    # Afficher le graphique
    plt.show(1)
    plt.show(2)

def nombre_commentaires_to_note():
    dico_nombre_comm_films_train = {}
    for comm_train in data_train :
        if comm_train[0] not in dico_nombre_comm_films_train.keys():
            dico_nombre_comm_films_train[comm_train[0]] = [1,[float(comm_train[2].replace(',', '.'))]]
        else : 
            dico_nombre_comm_films_train[comm_train[0]][0] += 1
            dico_nombre_comm_films_train[comm_train[0]][1].append(float(comm_train[2].replace(',', '.')))
    

    liste_train = list(dico_nombre_comm_films_train.values())

    #Pour le train on regarde les films en 10 notes et les films en 215 notes :
    film_10_train = []
    film_215_train = []
    for step in liste_train :
        if step[0] == 10 :
            film_10_train += step[1]
        elif step[0] == 215:
            film_215_train += step[1]

    # Compter le nombre d'occurrences de chaque note
    compteur_notes_10_train = Counter(film_10_train)
    compteur_notes_215_train = Counter(film_215_train)
    # Calculer le pourcentage d'apparition de chaque note
    total_notes_10_train = len(film_10_train)
    pourcentages_10_train = {note: (occurrences / total_notes_10_train) * 100 for note, occurrences in compteur_notes_10_train.items()}
    total_notes_215_train = len(film_215_train)
    pourcentages_215_train = {note: (occurrences / total_notes_215_train) * 100 for note, occurrences in compteur_notes_215_train.items()}
    sorted_pourcentages_10_train = dict(sorted(pourcentages_10_train.items()))
    sorted_pourcentages_215_train = dict(sorted(pourcentages_215_train.items()))

    # Extraire les clés et les valeurs du dictionnaire
    cles_10_train = list(sorted_pourcentages_10_train.keys())
    valeurs_10_train = list(sorted_pourcentages_10_train.values())
    cles_215_train = list(sorted_pourcentages_215_train.keys())
    valeurs_215_train = list(sorted_pourcentages_215_train.values())

    # Ajuster la largeur des barres et leur position
    largeur_barre = 0.35
    decalage = 0
    positions_10_train = range(len(cles_10_train))
    positions_215_train = [p + largeur_barre + decalage for p in positions_10_train]

    # Tracer l'histogramme
    plt.bar(positions_10_train, valeurs_10_train, color='green', width=largeur_barre, label="10 commentaires")
    plt.bar(positions_215_train, valeurs_215_train, color='orange', width=largeur_barre, label="215 commentaires")
    plt.title("Distributions des notes selon le nombre de commentaires")
    plt.xlabel("Notes")
    plt.ylabel("Pourcentages")
    plt.xticks(positions_10_train, cles_10_train, rotation=45)
    plt.legend()
    plt.tight_layout()

    # Afficher le graphique
    plt.grid(axis='y')
    plt.show()

def ecart_type():
    liste_note_train = []
    liste_note_dev = []
    for comm in data_train :
        liste_note_train.append(comm[2])
    for comm in data_dev :
        liste_note_dev.append(comm[2])

    compteur_notes_train = Counter(liste_note_train)
    liste_notes_freq_train = list(compteur_notes_train.items())
    compteur_notes_dev = Counter(liste_note_dev)
    liste_notes_freq_dev = list(compteur_notes_dev.items())
    
    liste_notes_etendue_train = [float(note.replace(',', '.')) for note, freq in liste_notes_freq_train for _ in range(freq)]
    ecart_type_train = np.std(liste_notes_etendue_train)
    print("Écart type train:", ecart_type_train)
    liste_notes_etendue_dev = [float(note.replace(',', '.')) for note, freq in liste_notes_freq_dev for _ in range(freq)]
    ecart_type_dev = np.std(liste_notes_etendue_dev)
    print("Écart type dev:", ecart_type_dev)

def caract():
    liste_comm_train = []
    liste_comm_dev = []

    for i in data_train:
        liste_comm_train.append(i[3])
    for i in data_dev:
        liste_comm_dev.append(i[3])


    string_train = ""
    string_dev = ""
    for c in liste_comm_train:
        string_train += " " + str(c)
    for c in liste_comm_dev:
        string_dev += " " + str(c)

    mots_train = re.findall(r'\b\w+\b', string_train)  # Utilisation d'une expression régulière pour trouver les mots
    nombre_de_mots_train = len(mots_train)
    mots_dev = re.findall(r'\b\w+\b', string_dev)  # Utilisation d'une expression régulière pour trouver les mots
    nombre_de_mots_dev = len(mots_dev)
    
    dict_mots_train = {}
    for m in mots_train : 
        if m not in dict_mots_train.keys():
            dict_mots_train[m] = 1
        else: dict_mots_train[m] += 1
    sorted_dict_mots_train = dict(sorted(dict_mots_train.items(),key=lambda x:x[1]))
    dict_mots_dev = {}
    for m in mots_dev : 
        if m not in dict_mots_dev.keys():
            dict_mots_dev[m] = 1
        else: dict_mots_dev[m] += 1
    sorted_dict_mots_dev = dict(sorted(dict_mots_dev.items(),key=lambda x:x[1]))

    print("Nombre de commentaires dans Train = " + str(len(liste_comm_train)))
    print("Nombre de mots dans Train = " + str(nombre_de_mots_train))
    print("Moyenne de mots par commentaire Train = " + str(nombre_de_mots_train/len(liste_comm_train)))
    print("\n")
    print("Nombre de commentaires dans Dev = " + str(len(liste_comm_dev)))
    print("Nombre de mots dans Dev = " + str(nombre_de_mots_dev))
    print("Moyenne de mots par commentaire Dev= " + str(nombre_de_mots_dev/len(liste_comm_dev)))
    print("\n")
    print("Les 3 mots les plus utilisé sont (hors mots outils): films, histoires et acteurs" )
    
#histogramme_note_globale()
#note_moyenne_film()
#boite_a_moustache()
#nombre_commentaires_to_note()
#ecart_type()
#caract()