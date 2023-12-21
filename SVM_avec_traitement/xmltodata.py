import xml.etree.ElementTree as ET
import pretraitement

#Charger le fichier xml

def xmltodata(fichier_xml):

    data = []

    # Charger le fichier XML
    tree = ET.parse(fichier_xml)
    root = tree.getroot()

    # Parcourir les éléments film et extraire les données
    for critique in root.findall('comment'):
        film = critique.find('movie').text
        user_id = critique.find('user_id').text
        note = critique.find('note').text
        commentaire = pretraitement.remove_french_stopwords(critique.find('commentaire').text)
        data.append([film,user_id,note,commentaire])
    return(data)

def xmltodata_test(fichier_xml):
    data = []

    # Charger le fichier XML
    tree = ET.parse(fichier_xml)
    root = tree.getroot()

    # Parcourir les éléments film et extraire les données
    for critique in root.findall('comment'):
        film = critique.find('movie').text
        user_id = critique.find('user_id').text
        commentaire = pretraitement.remove_french_stopwords(critique.find('commentaire').text)

        data.append([film,user_id,commentaire])
    return(data)

def review(fichier_xml):
    data = []

    # Charger le fichier XML
    tree = ET.parse(fichier_xml)
    root = tree.getroot()

    # Parcourir les éléments film et extraire les données
    for critique in root.findall('comment'):
        review = critique.find('review_id').text
        data.append(review)
    return(data)

