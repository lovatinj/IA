import xmltodata
import re

data_train = xmltodata.xmltodata("donnees_appr_dev/donnees_appr_dev/train.xml")
data_dev = xmltodata.xmltodata("donnees_appr_dev/donnees_appr_dev/dev.xml")
data_test = xmltodata.xmltodata_test("donnees_test/test.xml")

def Lexique():
    liste_comm_train = []
    liste_comm_dev = []
    liste_comm_test = []

    for i in data_train:
        liste_comm_train.append(i[3])
    for i in data_dev:
        liste_comm_dev.append(i[3])
    for i in data_test:
        liste_comm_test.append(i[2])

    string_train = ""
    string_dev = ""
    string_test = ""
    for c in liste_comm_train:
        string_train += " " + str(c)
    for c in liste_comm_dev:
        string_dev += " " + str(c)
    for c in liste_comm_test:
        string_test += " " + str(c)

    mots_train = re.findall(r'\b\w+\b', string_train)  # Utilisation d'une expression régulière pour trouver les mots
    mots_dev = re.findall(r'\b\w+\b', string_dev)  # Utilisation d'une expression régulière pour trouver les mots
    mots_test = re.findall(r'\b\w+\b', string_test)  # Utilisation d'une expression régulière pour trouver les mots


    lexique = {}
    cpt = 1

    for mot in mots_train:
        if mot not in lexique.keys(): 
            lexique[mot] = cpt
            cpt += 1
    for mot in mots_dev:
        if mot not in lexique.keys(): 
            lexique[mot] = cpt
            cpt += 1
    for mot in mots_test:
        if mot not in lexique.keys(): 
            lexique[mot] = cpt
            cpt += 1
    
    return(lexique)

