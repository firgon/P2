"""
classe qui s'occupe d'enregistrer les résultats de scrapping
"""
import csv


class Writer:

    # constructeur qui reçoit en argument le fichier et les entêtes de colonnes
    def __init__(self, fichier, entete):

        self.csvFile = open(fichier, 'w', newline='')
        self.writer = csv.DictWriter(self.csvFile, entete)

        self.writer.writeheader()

    def enregistre_nouvelle_page(self, donnees):
        print(donnees)
        self.writer.writerow(donnees)

    def close(self):
        self.csvFile.close();