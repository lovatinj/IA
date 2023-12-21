import xmltodata

data_test = xmltodata.review("donnees_test/test.xml")
classes_inverse = {0: '0,5', 1: '1,0', 2: '1,5', 3: '2,0', 4: '2,5', 5: '3,0', 6: '3,5', 7: '4,0', 8: '4,5', 9: '5,0'}

Fichier = open("to_platform.txt",'w')
string = ""

out = open("SVM_avec_traitement/out.txt","r")

for review in data_test:
    string += str(review) + " " + classes_inverse[int(out.readline()[:-1])] + "\n"

print(string)
Fichier.write(string)
Fichier.close()
