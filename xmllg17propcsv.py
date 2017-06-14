#!/usr/bin/python
from lxml import etree
import unicodecsv as csv

departements = ['03','15','19','23','43','63']
circos = ['01','02','03','04','05']
ficsv = open('lg017_propor_tour1.csv', 'w')

try:
	fieldnames = []
	fieldnames.extend(['circo', 'inscrits', 'votants', 'exprimes', 'abstentions', 'blancs', 'nuls','EXG','COM','FI','SOC','RDG','DVG','ECO','DIV','REG','REM','MDM','UDI','LR','DVD','DLF','FN','EXD'])
	majcsv = csv.DictWriter(ficsv, fieldnames = fieldnames)
	majcsv.writeheader()
	for dep in departements:
		for circo in circos:
			try:
				arbre = etree.parse("http://elections.interieur.gouv.fr/telechargements/LG2017/resultatsT1/0"+dep+"/0"+dep+circo+".xml")
				print ("dep OK")
				for noeud in arbre.xpath("//Election/Departement/Circonscription"):
					objet = {}
					for circ in noeud.xpath("CodCirLg"):
						objet["circo"] = dep + circ.text
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
							for nuance in liste.xpath("CodNua"):
								nu = nuance.text
							for voix in liste.xpath("NbVoix"):
								vox = int(voix.text)
							objet[nu] = vox
						#print(objet)
						majcsv.writerow(objet)
			except:
				continue
finally:
	ficsv.close()