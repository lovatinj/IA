import xmltodata
import Lexique_SVM
import re

lexique = Lexique_SVM.Lexique()
data_test = xmltodata.xmltodata_test("donnees_test/test.xml")
classes = {"0,5":0, "1,0":1, "1,5":2, "2,0":3, "2,5":4, "3,0":5, "3,5":6, "4,0":7, "4,5":8, "5,0":9}

liste_comm_test = []
for i in data_test:
    liste_comm_test.append(("0,5", i[2]))

# Classificateur SVM de Test
SVM_test = open("SVM_test.svm", 'w')
svm_test = ""

for critique_en_cours in liste_comm_test:
    string = str(classes[critique_en_cours[0]]) + " "
    if critique_en_cours[1] is not None:
        mots_courants = re.findall(r'\b\w+\b', critique_en_cours[1])
        dico_courant = {}
        for mot in mots_courants:
            if lexique[mot] not in dico_courant:
                dico_courant[lexique[mot]] = 1
            else:
                dico_courant[lexique[mot]] += 1
        dico_courant_order = dict(sorted(dico_courant.items()))

        for key in dico_courant_order:
            string += str(key) + ":" + str(dico_courant_order[key]) + " "
        string += "\n"
        svm_test += string

SVM_test.write(svm_test)
SVM_test.close()
