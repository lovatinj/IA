import xmltodata
import re
import Lexique_SVM

lexique = Lexique_SVM.Lexique()
classes = {"0,5":0, "1,0":1, "1,5":2, "2,0":3, "2,5":4, "3,0":5, "3,5":6, "4,0":7, "4,5":8, "5,0":9}

data_train = xmltodata.xmltodata("donnees_appr_dev/donnees_appr_dev/train.xml")
data_dev = xmltodata.xmltodata("donnees_appr_dev/donnees_appr_dev/dev.xml")

liste_comm_train = []
liste_comm_dev = []

for i in data_train:
    liste_comm_train.append((i[2],i[3]))
for i in data_dev:
    liste_comm_dev.append((i[2],i[3]))

#Classificateur SVM de Train
SVM_train = open("SVM_train.svm",'w')
svm_train = ""

for critique_en_cours in liste_comm_train:
    string = str(classes[critique_en_cours[0]]) + " "
    if critique_en_cours[1] != None :
        mots_courants = re.findall(r'\b\w+\b', critique_en_cours[1])
        dico_courant = {}
        for i in mots_courants:
            if lexique[i] not in dico_courant.keys(): dico_courant[lexique[i]] = 1
            else : dico_courant[lexique[i]] += 1
        dico_courant_order = dict(sorted(dico_courant.items()))
        
        for key in dico_courant_order:
            string += str(key) + ":" + str(dico_courant_order[key]) + " "
        string += "\n"
        svm_train += string

SVM_train.write(svm_train)
SVM_train.close()

#Classificateur SVM de Dev
SVM_dev = open("SVM_dev.svm",'w')
svm_dev = ""

for critique_en_cours in liste_comm_dev:
    string = str(classes[critique_en_cours[0]]) + " "
    if critique_en_cours[1] != None :
        mots_courants = re.findall(r'\b\w+\b', critique_en_cours[1])
        dico_courant = {}
        for i in mots_courants:
            if lexique[i] not in dico_courant.keys(): dico_courant[lexique[i]] = 1
            else : dico_courant[lexique[i]] += 1
        dico_courant_order = dict(sorted(dico_courant.items()))
        
        for key in dico_courant_order:
            string += str(key) + ":" + str(dico_courant_order[key]) + " "
        string += "\n"
        svm_dev += string

SVM_dev.write(svm_dev)
SVM_dev.close()