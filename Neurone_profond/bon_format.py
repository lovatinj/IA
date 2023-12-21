
import xmltodata

def round_to_half(value):
    return round(value * 2) / 2

id = []
note = []

data_test = xmltodata.review("test.xml")
for review in data_test:
    id.append(str(review))

out = open("out.txt","r")
for la in out :
    note.append(str(round_to_half(float(la))).replace('.', ','))

Fichier = open("to_platform.txt",'w')
string = ""
for i in range(0,len(id)):
    string += id[i] + " " + note[i] + "\n"

print(string)
Fichier.write(string)
Fichier.close()