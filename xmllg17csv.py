#!/usr/bin/python
from lxml import etree
import unicodecsv as csv

#code departement
departement = '89'
#code circo
circo = '02'
#generation code commune de 000 -> 499
communes = ["%03d" % i for i in range(1,500)]
ficsv = open('lg017_yonne_circo2_test_tour1.csv', 'w')

try:
	for com in communes:
		try:
			fieldnames = []
			fieldnames.extend(['code insee', 'ville', 'inscrits', 'votants', 'exprimes', 'abstentions', 'blancs', 'nuls'])
			arbre = etree.parse("http://elections.interieur.gouv.fr/telechargements/LG2017/resultatsT1/0"+departement+"/0"+departement+circo+com+".xml")
			print ("header OK")
			for noeud in arbre.xpath("//Election/Departement/Commune"):
				for resultats in noeud.xpath("Tours/Tour[NumTour=1]"):
					for liste in resultats.xpath("Resultats/Candidats/Candidat"):
						nu = ''
						for nuance in liste.xpath("NomPsn"):
							nu = nuance.text
						fieldnames.extend([nu])
			majcsv = csv.DictWriter(ficsv, fieldnames = fieldnames)
			majcsv.writeheader()
		except:
			continue
		break
	for com in communes:
		try:
			arbre = etree.parse("http://elections.interieur.gouv.fr/telechargements/LG2017/resultatsT1/0"+departement+"/0"+departement+circo+com+".xml")
			print ("commune OK") 
			for noeud in arbre.xpath("//Election/Departement/Commune"):
				objet = {}
				for insee in noeud.xpath("CodSubCom"):
					objet["code insee"] = departement + insee.text
				for commune in noeud.xpath("LibSubCom"):
					objet["ville"] = commune.text
				for resultats in noeud.xpath("Tours/Tour[NumTour=1]"):
					for inscrits in resultats.xpath("Mentions/Inscrits/Nombre"):
						objet["inscrits"] = int(inscrits.text)
					for abstentions in resultats.xpath("Mentions/Abstentions/Nombre"):
						objet["abstentions"] = int(abstentions.text)
					for votants in resultats.xpath("Mentions/Votants/Nombre"):
						objet["votants"] = int(votants.text)
					for blancs in resultats.xpath("Mentions/Blancs/Nombre"):
						objet["blancs"] = int(blancs.text)
					for nuls in resultats.xpath("Mentions/Nuls/Nombre"):
						objet["nuls"] = int(nuls.text)
					for exprimes in resultats.xpath("Mentions/Exprimes/Nombre"):
						objet["exprimes"] = int(exprimes.text)
					for liste in resultats.xpath("Resultats/Candidats/Candidat"):
						nu = ''
						vox = 0
						for nuance in liste.xpath("NomPsn"):
							nu = nuance.text
						for voix in liste.xpath("RapportExprime"):
							vox = voix.text.strip()
						objet[nu] = vox
					#print(objet)
					majcsv.writerow(objet)
		except:
			continue

except:
	print('hum erreur')

finally:
	ficsv.close()