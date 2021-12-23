import pdfplumber
import re
from pprint import pprint


pdf_file = pdfplumber.open('RapportPDF_2.pdf')
pdf_page = pdf_file.pages[0]

pdf_text = pdf_page.extract_text()

# Identification
identification = {}
try:
	Adresse = re.search(r'Adresse: (.*?)\n',pdf_text).group(1)
	identification['Adresse'] = Adresse
except Exception as e:
	print(e,'==>','Adresse')
	Adresse = None
	
	# ===========================>>>>>>>>>>>>>>>>>>>

try:
	Arrondissement = re.search('Arrondissement: (.*?)\n',pdf_text).group(1)
	identification['Arrondissement'] = Arrondissement
except Exception as e:
	print(e,'==>','Arrondissement')
	Arrondissement = None
	
	# ===========================>>>>>>>>>>>>>>>>>>>

try:
	Cadastre_et_numéro_de_lot = re.search(r'Cadastre\(s\) et numéro\(s\)de lot : ([\d ]+)',pdf_text).group(1)
	identification['Cadastre_et_numéro_de_lot'] = Cadastre_et_numéro_de_lot

except Exception as e:
	print(e,'==>','Cadastre_et_numéro_de_lot')
	Cadastre_et_numéro_de_lot = None
	
	# ===========================>>>>>>>>>>>>>>>>>>>

try:
	Numéro_matricule = re.search(r'Numéro matricule: ([\d -]+)',pdf_text).group(1)
	identification['Numéro_matricule'] = Numéro_matricule
except Exception as e:
	print(e,'==>','Numéro_matricule')
	Numéro_matricule = None
	
	# ===========================>>>>>>>>>>>>>>>>>>>

try:
	Utilisation_prédominante = re.search(r'Utilisation prédominante: (.*?)\n',pdf_text).group(1)
	identification['Utilisation_prédominante'] = Utilisation_prédominante

except Exception as e:
	print(e,'==>','Utilisation_prédominante')
	Utilisation_prédominante = None
	
	# ===========================>>>>>>>>>>>>>>>>>>>

try:
	numero_de_unite = re.search(r'Numéro d\'unité de voisinage: ([\d -]+)',pdf_text).group(1)
	identification['numero_de_unite'] = numero_de_unite

except Exception as e:
	print(e,'==>','numero_de_unite')
	numero_de_unite = None
	
	# ===========================>>>>>>>>>>>>>>>>>>>

try:
	dossier_evaluation = re.search(r'Dossier d\'évaluation No: ([\d -]+)',pdf_text).group(1)
	identification['dossier_evaluation'] = dossier_evaluation

except Exception as e:
	print(e,'==>','dossier_evaluation')
	dossier_evaluation = None
	
	# ===========================>>>>>>>>>>>>>>>>>>>


# Propriétaire
proprieataire = {}
try:
	nom = re.search(r'Nom: (.*?)\n',pdf_text).group(1)
	proprieataire['nom'] = nom
except Exception as e:
	print(e,'==>','nom')
	nom = None
	
	# ===========================>>>>>>>>>>>>>>>>>>>

try:
	Statut_aux_fins_imposition_scolaire = re.search(r'Statut aux fins d\'imposition scolaire: (.*?)\n',pdf_text).group(1)
	proprieataire['Statut_aux_fins_imposition_scolaire'] = Statut_aux_fins_imposition_scolaire

except Exception as e:
	print(e,'==>','Statut_aux_fins_imposition_scolaire')
	Statut_aux_fins_imposition_scolaire = None
	
	# ===========================>>>>>>>>>>>>>>>>>>>

try:
	adresse_postale = re.search(r'Adresse postale: (.*?)\n',pdf_text).group(1)
	proprieataire['adresse_postale'] = adresse_postale

except Exception as e:
	print(e,'==>','adresse_postale')
	adresse_postale = None
	
	# ===========================>>>>>>>>>>>>>>>>>>>

try:
	Municipalité =re.search(r'Municipalité: (.*?)\n',pdf_text).group(1)
	proprieataire['Municipalité'] = Municipalité

except Exception as e:
	print(e,'==>','Municipalité')
	Municipalité = None
	
	# ===========================>>>>>>>>>>>>>>>>>>>

try:
	date_inscription = re.search(r'Date d\'inscription au rôle: ([\d -]+)',pdf_text).group(1)
	proprieataire['date_inscription'] = date_inscription

except Exception as e:
	print(e,'==>','date_inscription')
	date_inscription = None
	
	# ===========================>>>>>>>>>>>>>>>>>>>


# Caractéristiques de l'unité d'évaluation

evalution = {}
try:
	mesure_frontale = re.search(r'Mesure frontale: ([\d, m]+)',pdf_text).group(1)
	evalution['mesure_frontale'] = mesure_frontale

except Exception as e:
	print(e,'==>','mesure_frontale')
	mesure_frontale = None
	
	# ===========================>>>>>>>>>>>>>>>>>>>

try:
	nombre_etages = re.search(r'Nombre d\'étages: ([\d]+)\n',pdf_text).group(1)
	evalution['nombre_etages'] = nombre_etages

except Exception as e:
	print(e,'==>','nombre_etages')
	nombre_etages = None
	
	# ===========================>>>>>>>>>>>>>>>>>>>

try:
	Superficie = re.search(r'Superficie: ([\d, m]+)',pdf_text).group(1)
	evalution['Superficie'] = Superficie

except Exception as e:
	print(e,'==>','Superficie')
	Superficie = None
	
	# ===========================>>>>>>>>>>>>>>>>>>>

try:
	annee_de_construction = re.search(r'Année de construction: ([\d, m]+)',pdf_text).group(1)
	evalution['annee_de_construction'] = annee_de_construction

except Exception as e:
	print(e,'==>','annee_de_construction')
	annee_de_construction = None
	
	# ===========================>>>>>>>>>>>>>>>>>>>

try:
	aire_etages = re.search(r'Aire d\'étages: ([\d, m]+)',pdf_text).group(1)
	evalution['aire_etages'] = aire_etages

except Exception as e:
	print(e,'==>','aire_etages')
	aire_etages = None
	
	# ===========================>>>>>>>>>>>>>>>>>>>

try:
	genere_construction = re.search(r'Genre de construction: (.*?)\n',pdf_text).group(1)
	evalution['genere_construction'] = genere_construction

except Exception as e:
	print(e,'==>','genere_construction')
	genere_construction = None
	
	# ===========================>>>>>>>>>>>>>>>>>>>

try:
	lien_physique = re.search(r'Lien physique: (.*?)\n',pdf_text).group(1)
	evalution['lien_physique'] = lien_physique

except Exception as e:
	print(e,'==>','lien_physique')
	lien_physique = None
	
	# ===========================>>>>>>>>>>>>>>>>>>>

try:
	nombre_logement = re.search(r'Nombre de logements: ([\d ]+)\n',pdf_text).group(1)
	evalution['nombre_logement'] = nombre_logement

except Exception as e:
	print(e,'==>','nombre_logement')
	nombre_logement = None
	
	# ===========================>>>>>>>>>>>>>>>>>>>

try:
	Nombre_de_locaux_non_residentiels = re.search(r'Nombre de locaux non residentiels: ([\d ]+)\n',pdf_text).group(1)
	evalution['Nombre_de_locaux_non_residentiels'] = Nombre_de_locaux_non_residentiels
except Exception as e:
	print(e,'==>','Nombre_de_locaux_non_residentiels')
	Nombre_de_locaux_non_residentiels = None
	
	# ===========================>>>>>>>>>>>>>>>>>>>

try:
	Nombre_de_chambres_locatives = re.search(r'Nombre de chambres locatives: ([\d ]+)\n',pdf_text).group(1)
	evalution['Nombre_de_chambres_locatives'] = Nombre_de_chambres_locatives
except Exception as e:
	print(e,'==>','Nombre_de_chambres_locatives')
	Nombre_de_chambres_locatives = None
	
	# ===========================>>>>>>>>>>>>>>>>>>>


# Valeurs au rôle d'évaluation
valeur_evaluation = {}
try:
	date_reference_au_marche = re.search(r'Date de référence au marché: ([\d -]+)\n',pdf_text).group(1)
	valeur_evaluation['date_reference_au_marche'] = date_reference_au_marche
except Exception as e:
	print(e,'==>','date_reference_au_marche')
	date_reference_au_marche = None
	
	# ===========================>>>>>>>>>>>>>>>>>>>

try:
	valeur_terrain = re.search(r'Valeur du terrain: ([\d ]+\$)\n',pdf_text).group(1)
	valeur_evaluation['valeur_terrain'] = valeur_terrain
except Exception as e:
	print(e,'==>','valeur_terrain')
	valeur_terrain = None
	
	# ===========================>>>>>>>>>>>>>>>>>>>

try:
	valeur_batiment = re.search(r'Valeur du bâtiment: ([\d ]+\$)\n',pdf_text).group(1)
	valeur_evaluation['valeur_batiment'] = valeur_batiment

except Exception as e:
	print(e,'==>','valeur_batiment')
	valeur_batiment = None
	
	# ===========================>>>>>>>>>>>>>>>>>>>

try:
	valeur_immeuble = re.search(r'Valeur de l\'immeuble: ([\d ]+\$)\n',pdf_text).group(1)
	valeur_evaluation['valeur_immeuble'] = valeur_immeuble

except Exception as e:
	print(e,'==>','valeur_immeuble')
	valeur_immeuble = None
	
	# ===========================>>>>>>>>>>>>>>>>>>>

try:
	Valeur_de_immeuble_au_rôle_antérieur = re.search(r'Valeur de l\'immeuble au rôle antérieur: ([\d ]+\$)\n',pdf_text).group(1)
	valeur_evaluation['Valeur_de_immeuble_au_rôle_antérieur'] = Valeur_de_immeuble_au_rôle_antérieur
except Exception as e:
	print(e,'==>','Valeur_de_immeuble_au_rôle_antérieur')
	Valeur_de_immeuble_au_rôle_antérieur = None
	
	# ===========================>>>>>>>>>>>>>>>>>>>



# Répartition fiscale
fiscale = {}
try:
	Catégorie_et_classe_d_immeuble_à_des_fins_d_application_des_taux_variés_de_taxation = re.search(r'taxation : (.*?)\n',pdf_text).group(1)
	fiscale['Catégorie_et_classe_d_immeuble_à_des_fins_d_application_des_taux_variés_de_taxation'] = Catégorie_et_classe_d_immeuble_à_des_fins_d_application_des_taux_variés_de_taxation
except Exception as e:
	print(e,'==>','Catégorie_et_classe_d_immeuble_à_des_fins_d_application_des_taux_variés_de_taxation')
	Catégorie_et_classe_d_immeuble_à_des_fins_d_application_des_taux_variés_de_taxation = None
	
	# ===========================>>>>>>>>>>>>>>>>>>>

try:
	immuble = re.search(r'Immeuble: (.*?)\n',pdf_text).group(1)
	fiscale['immuble'] = immuble
except Exception as e:
	print(e,'==>','immuble')
	immuble = None
	
	# ===========================>>>>>>>>>>>>>>>>>>>

try:
	Valeur_imposable = re.search(r'Valeur imposable: ([\d ]+\$)',pdf_text).group(1)
	fiscale['Valeur_imposable'] = Valeur_imposable
except Exception as e:
	print(e,'==>','Valeur_imposable')
	Valeur_imposable = None
	
	# ===========================>>>>>>>>>>>>>>>>>>>

try:
	Valeur_non_imposable = re.search(r'Valeur non imposable: ([\d ]+\$)',pdf_text).group(1)
	fiscale['Valeur_non_imposable'] = Valeur_non_imposable
except Exception as e:
	print(e,'==>','Valeur_non_imposable')
	Valeur_non_imposable = None
	
	# ===========================>>>>>>>>>>>>>>>>>>>

	
item = {
	'Identification_de_l_unité_d_évaluation' : identification,
	'Propriétaire' : proprieataire,
	'Caractéristiques _e l_unité d_évaluation' : evalution,
	'Valeurs_au_rôle_d_évaluation' : valeur_evaluation,
	'Répartition_fiscale' : fiscale
}

print(item)

