import random
import json

# ===============================================
# SECTION 1: CONFIGURATION ET CONSTANTES
# ===============================================

# Dictionnaire des classes disponibles (lettre -> nom complet)
dicoClasse = {"G": "Guerrier", "P": "Paladin", "B": "Barbare",
              "D": "Druide", "V": "Voleur", "M": "Mage"}

# Liste des attributs du personnage (code, nom complet)
ATTRS = [("F", "Force"), ("H", "Habileté"), ("E", "Endurance"),
         ("I", "Intelligence"), ("S", "Sagesse"), ("C", "Charisme")]

# Règles pour les attributs
MIN_ATTR = 1    # Minimum pour chaque attribut
MAX_ATTR = 5    # Maximum pour chaque attribut
TOTAL_POINTS = 18  # Total de points à répartir

# ===============================================
# SECTION 2: FONCTIONS DE CRÉATION DU PERSONNAGE
# ===============================================

def choisir_classe():
    """Permet au joueur de choisir une classe"""
    print("\n=== CHOIX DE LA CLASSE ===")
    while True:  # Boucle jusqu'à avoir un choix valide
        print("Classes disponibles :")
        # Afficher toutes les options
        for lettre, nom_classe in dicoClasse.items():
            print(f"  {lettre} - {nom_classe}")

        # Demander le choix
        choix = input("Tapez la lettre de votre choix : ").upper()

        # Vérifier si le choix est valide
        if choix in dicoClasse:
            return dicoClasse[choix]  # Retourner le nom de la classe
        else:
            print("Choix invalide ! Réessayez.\n")

def generer_attributs():
    """Crée des attributs aléatoires qui respectent les règles du jeu"""
    # Commencer avec 1 point dans chaque attribut (le minimum)
    attributs = [1, 1, 1, 1, 1, 1]

    # Calculer combien de points il reste à distribuer
    points_restants = TOTAL_POINTS - 6  # 18 - 6 = 12 points

    # Distribuer les points restants un par un
    for _ in range(points_restants):
        # Trouver quels attributs peuvent encore recevoir des points
        indices_possibles = []
        for i in range(6):
            if attributs[i] < MAX_ATTR:  # Si pas encore au maximum
                indices_possibles.append(i)

        # Ajouter 1 point à un attribut choisi au hasard
        if indices_possibles:
            attribut_choisi = random.choice(indices_possibles)
            attributs[attribut_choisi] += 1

    return attributs

def generer_attributs_optimises(classe):
    """Crée des attributs optimisés selon la classe choisie"""
    # Commencer avec 1 point dans chaque attribut (le minimum)
    attributs = [1, 1, 1, 1, 1, 1]  # F, H, E, I, S, C

    # Définir les attributs principaux selon la classe
    if classe in ["Guerrier", "Barbare"]:
        # Force (0) et Endurance (2) au maximum
        attributs[0] = 5  # Force
        attributs[2] = 5  # Endurance
    elif classe == "Paladin":
        # Charisme (5) et Sagesse (4) au maximum
        attributs[5] = 5  # Charisme
        attributs[4] = 5  # Sagesse
    elif classe == "Voleur":
        # Habileté (1) et Endurance (2) au maximum
        attributs[1] = 5  # Habileté
        attributs[2] = 5  # Endurance
    elif classe == "Druide":
        # Sagesse (4) et Intelligence (3) au maximum
        attributs[4] = 5  # Sagesse
        attributs[3] = 5  # Intelligence
    elif classe == "Mage":
        # Intelligence (3) et Charisme (5) au maximum
        attributs[3] = 5  # Intelligence
        attributs[5] = 5  # Charisme

    # Calculer les points restants et les répartir
    points_utilises = sum(attributs)
    points_restants = TOTAL_POINTS - points_utilises

    # Distribuer les points restants sur les autres attributs
    for _ in range(points_restants):
        indices_possibles = []
        for i in range(6):
            if attributs[i] < MAX_ATTR:
                indices_possibles.append(i)

        if indices_possibles:
            attribut_choisi = random.choice(indices_possibles)
            attributs[attribut_choisi] += 1

    return attributs

def choisir_type_attributs():
    """Demande au joueur comment il veut générer ses attributs"""
    print("\n=== GÉNÉRATION DES ATTRIBUTS ===")
    while True:
        print("Comment voulez-vous créer vos attributs ?")
        print("  1 - Aléatoire (répartition au hasard)")
        print("  2 - Optimisé pour votre classe")

        choix = input("Tapez 1 ou 2 : ")

        if choix == "1":
            return "aleatoire"
        elif choix == "2":
            return "optimise"
        else:
            print("Choix invalide ! Tapez 1 ou 2.\n")

def creer_personnage(nom, classe, type_attributs):
    """Crée un personnage complet avec tous ses détails"""
    # Générer les valeurs d'attributs selon le type choisi
    if type_attributs == "optimise":
        valeurs_attributs = generer_attributs_optimises(classe)
    else:
        valeurs_attributs = generer_attributs()

    # Créer un dictionnaire pour les attributs (plus facile à lire)
    mes_attributs = {}
    for i in range(len(ATTRS)):
        nom_attribut = ATTRS[i][1]  # Prendre le nom complet
        valeur = valeurs_attributs[i]
        mes_attributs[nom_attribut] = valeur

    # Inventaire de départ avec équipement de base
    inventaire_depart = [
        {
            "nom": "Vêtements",
            "type": "armure",
            "prix": 0,
            "stats": {"defense": 1},
            "description": "Vêtements simples",
            "slot": "torse",
            "porte": True
        },
        {
            "nom": "Dague",
            "type": "arme",
            "prix": 15,
            "stats": {"degats": 3, "precision": 85},
            "description": "Une dague simple mais efficace",
            "slot": "main_droite",
            "porte": True
        }
    ]

    # Créer le personnage final
    mon_personnage = {
        "nom": nom,
        "classe": classe,
        "attributs": mes_attributs,
        "total_points": sum(valeurs_attributs),
        "type_creation": type_attributs,
        "experience": 0,
        "pieces_or": 50,  # Un peu d'argent de départ
        "inventaire": inventaire_depart,
        "points_de_vie_actuels": 10 + (mes_attributs.get("Endurance", 1) * 3) # Initialiser les PV actuels
    }

    return mon_personnage

# ===============================================
# SECTION 3: FONCTIONS SAUVEGARDE/CHARGEMENT JSON
# ===============================================

def sauvegarder_personnage(personnage):
    """Sauvegarde un personnage dans un fichier JSON"""
    nom_fichier = f"personnage_{personnage['nom'].lower().replace(' ', '_')}.json"
    try:
        with open(nom_fichier, 'w', encoding='utf-8') as fichier:
            json.dump(personnage, fichier, indent=2, ensure_ascii=False)
        print(f"Personnage sauvegardé dans {nom_fichier}")
        return True
    except Exception as e:
        print(f"Erreur lors de la sauvegarde : {e}")
        return False

def charger_personnage(nom_fichier=None):
    """Charge un personnage depuis un fichier JSON"""
    if nom_fichier is None:
        # Afficher d'abord la liste des personnages disponibles
        fichiers_personnages = lister_personnages_sauvegardes()

        if not fichiers_personnages:
            return None

        print("\nChoisissez un personnage à charger :")
        try:
            choix = int(input("Numéro du personnage (0 pour annuler) : "))
            if choix == 0:
                return None
            if 1 <= choix <= len(fichiers_personnages):
                nom_fichier = fichiers_personnages[choix - 1]
            else:
                print("Choix invalide")
                return None
        except ValueError:
            print("Veuillez entrer un numéro valide")
            return None

    try:
        with open(nom_fichier, 'r', encoding='utf-8') as fichier:
            personnage = json.load(fichier)
        print(f"Personnage {personnage['nom']} chargé avec succès !")
        # Assurer que points_de_vie_actuels existe, sinon le calculer
        if 'points_de_vie_actuels' not in personnage:
            stats_base = calculer_stats_personnage(personnage)
            personnage['points_de_vie_actuels'] = stats_base['pv']
        return personnage
    except FileNotFoundError:
        print(f"Aucun personnage trouvé avec ce nom.")
        return None
    except json.JSONDecodeError:
        print("Erreur : Le fichier de sauvegarde est corrompu")
        return None

def lister_personnages_sauvegardes():
    """Liste tous les fichiers de personnages sauvegardés"""
    import os
    fichiers_personnages = [f for f in os.listdir('.') if f.startswith('personnage_') and f.endswith('.json')]
    if fichiers_personnages:
        print("\nPersonnages sauvegardés :")
        for i, fichier in enumerate(fichiers_personnages, 1):
            nom = fichier.replace('personnage_', '').replace('.json', '').replace('_', ' ').title()
            print(f"{i}. {nom}")
        return fichiers_personnages
    else:
        print("Aucun personnage sauvegardé trouvé.")
        return []

def afficher_details_personnage(personnage):
    """Affiche tous les détails d'un personnage"""
    if personnage is None:
        print("Aucun personnage chargé !")
        return
    
    print(f"\n=== DÉTAILS DE {personnage['nom'].upper()} ===")
    print(f"Classe : {personnage['classe']}")
    print(f"Expérience : {personnage['experience']} XP")
    print(f"Pièces d'or : {personnage['pieces_or']}")
    
    # Calculer et afficher les statistiques
    stats = calculer_stats_personnage(personnage)
    pv_actuels = personnage.get('points_de_vie_actuels', stats['pv'])
    
    print(f"\n=== STATISTIQUES ===")
    print(f"Points de vie : {pv_actuels}/{stats['pv']}")
    if pv_actuels <= 0:
        print("💀 STATUT : MORT 💀")
    else:
        print("❤️  STATUT : VIVANT")
    print(f"Attaque : {stats['attaque']}")
    print(f"Défense : {stats['defense']}")
    
    print(f"\n=== ATTRIBUTS ===")
    for nom_attr, valeur in personnage['attributs'].items():
        print(f"{nom_attr} : {valeur}")
    print(f"Total des points : {personnage['total_points']}/18")
    
    # Afficher l'équipement porté
    equipement_porte = [obj for obj in personnage['inventaire'] if obj.get('porte', False)]
    
    if equipement_porte:
        print(f"\n=== ÉQUIPEMENT PORTÉ ===")
        for objet in equipement_porte:
            stats_str = ""
            if objet['stats']:
                stats_list = []
                for stat, val in objet['stats'].items():
                    if val > 0:
                        stats_list.append(f"+{val} {stat}")
                    elif val < 0:
                        stats_list.append(f"{val} {stat}")
                if stats_list:
                    stats_str = f" ({', '.join(stats_list)})"
            print(f"  {objet['nom']} [{objet['slot']}]{stats_str}")
    else:
        print(f"\n=== ÉQUIPEMENT PORTÉ ===")
        print("Aucun équipement porté")
    
    # Afficher le nombre d'objets dans l'inventaire
    objets_non_equipes = len([obj for obj in personnage['inventaire'] if not obj.get('porte', False)])
    print(f"\n=== INVENTAIRE ===")
    print(f"Objets en inventaire : {objets_non_equipes}")
    print(f"Total d'objets : {len(personnage['inventaire'])}")

def menu_personnage():
    """Menu pour gérer les personnages"""
    global personnage_actuel
    while True:
        print("\n=== GESTION DES PERSONNAGES ===")
        print("1. Créer un nouveau personnage")
        print("2. Charger un personnage existant")
        print("3. Lister les personnages sauvegardés")
        print("4. Voir les détails du personnage actuel")
        print("5. Retour au menu principal")

        choix = input("Votre choix (1-5) : ")

        if choix == "1":
            # Créer un nouveau personnage
            nom_personnage = input("Quel est le nom de votre personnage ? ")
            classe_choisie = choisir_classe()
            type_attributs = choisir_type_attributs()
            personnage = creer_personnage(nom_personnage, classe_choisie, type_attributs)

            # Afficher le personnage créé
            print(f"\n=== PERSONNAGE CREE ===")
            print(f"Nom : {personnage['nom']}")
            print(f"Classe : {personnage['classe']}")
            print(f"Type : Attributs {personnage['type_creation']}s")
            print(f"\nAttributs :")
            for nom_attr, valeur in personnage['attributs'].items():
                print(f"   {nom_attr} : {valeur}")
            print(f"\nTotal des points utilisés : {personnage['total_points']}/18")
            print(f"Experience : {personnage['experience']}")
            print(f"Pieces d'or : {personnage['pieces_or']}")
            print(f"Équipement de départ : {', '.join([obj['nom'] for obj in personnage['inventaire']])}")

            # Proposer la sauvegarde
            sauver = input("\nVoulez-vous sauvegarder ce personnage ? (o/n) : ")
            if sauver.lower() in ['o', 'oui', 'y', 'yes']:
                if sauvegarder_personnage(personnage):
                    return personnage
            return personnage

        elif choix == "2":
            personnage = charger_personnage()
            if personnage:
                return personnage

        elif choix == "3":
            lister_personnages_sauvegardes()

        elif choix == "4":
            # Afficher les détails du personnage actuel
            afficher_details_personnage(personnage_actuel)

        elif choix == "5":
            return None

        else:
            print("Choix invalide")

# ===============================================
# SECTION 4: FONCTIONS BOUTIQUE ET INVENTAIRE
# ===============================================

def charger_boutique():
    """Charge la base de données des objets de la boutique"""
    try:
        with open('boutique.json', 'r', encoding='utf-8') as fichier:
            boutique = json.load(fichier)
        return boutique
    except FileNotFoundError:
        print("Erreur : Le fichier boutique.json n'a pas été trouvé")
        return []
    except json.JSONDecodeError:
        print("Erreur : Le fichier boutique.json est mal formaté")
        return []

def afficher_objet(objet):
    """Affiche les détails d'un objet"""
    print(f"\n=== {objet['nom']} ===")
    print(f"Type : {objet['type'].title()}")
    print(f"Prix : {objet['prix']} pièces d'or")
    print(f"Description : {objet['description']}")
    print(f"Emplacement : {objet['slot']}")
    if objet['stats']:
        print("Statistiques :")
        for stat, valeur in objet['stats'].items():
            if valeur > 0:
                print(f"  +{valeur} {stat}")
            elif valeur < 0:
                print(f"  {valeur} {stat}")
            else:
                print(f"  {stat}: {valeur}")

def peut_porter_objet(personnage, objet):
    """Vérifie si le personnage peut porter cet objet (slot libre ou remplaçable)"""
    slot = objet['slot']

    # Les objets sans slot (consommables) peuvent toujours être ajoutés
    if slot == "aucun":
        return True

    # Vérifier si le slot est déjà occupé
    for item in personnage['inventaire']:
        if item.get('porte', False) and item['slot'] == slot:
            if slot == "deux_mains":
                # Vérifier aussi main_droite et main_gauche
                return not any(i.get('porte', False) and i['slot'] in ['main_droite', 'main_gauche']
                              for i in personnage['inventaire'])
            return True  # Peut remplacer l'objet existant

    # Si l'objet nécessite deux mains, vérifier que les deux mains sont libres
    if slot == "deux_mains":
        mains_occupees = any(i.get('porte', False) and i['slot'] in ['main_droite', 'main_gauche']
                            for i in personnage['inventaire'])
        return not mains_occupees

    return True

def equiper_objet(personnage, nom_objet):
    """Équipe un objet de l'inventaire"""
    for objet in personnage['inventaire']:
        if objet['nom'] == nom_objet and not objet.get('porte', False):
            slot = objet['slot']

            if slot == "aucun":
                print("Cet objet ne peut pas être équipé")
                return False

            # Déséquiper les objets du même slot
            for item in personnage['inventaire']:
                if item.get('porte', False) and item['slot'] == slot:
                    item['porte'] = False
                    print(f"{item['nom']} déséquipé")

                # Cas spécial pour les armes à deux mains
                if slot == "deux_mains" and item.get('porte', False) and item['slot'] in ['main_droite', 'main_gauche']:
                    item['porte'] = False
                    print(f"{item['nom']} déséquipé")

            objet['porte'] = True
            print(f"{nom_objet} équipé avec succès !")
            return True

    print("Objet non trouvé dans l'inventaire")
    return False

def desequiper_objet(personnage, nom_objet):
    """Déséquipe un objet"""
    for objet in personnage['inventaire']:
        if objet['nom'] == nom_objet and objet.get('porte', False):
            objet['porte'] = False
            print(f"{nom_objet} déséquipé avec succès !")
            return True

    print("Objet non trouvé ou non équipé")
    return False

def acheter_objet(personnage, objet):
    """Achète un objet de la boutique"""
    if personnage['pieces_or'] >= objet['prix']:
        personnage['pieces_or'] -= objet['prix']

        # Créer une copie de l'objet pour l'inventaire
        nouvel_objet = objet.copy()
        nouvel_objet['porte'] = False

        personnage['inventaire'].append(nouvel_objet)
        print(f"{objet['nom']} acheté pour {objet['prix']} pièces d'or !")
        return True
    else:
        print(f"Pas assez d'argent ! Il vous faut {objet['prix']} pièces d'or (vous avez {personnage['pieces_or']})")
        return False

def vendre_objet(personnage, nom_objet):
    """Vend un objet de l'inventaire à 50% de sa valeur"""
    for i, objet in enumerate(personnage['inventaire']):
        if objet['nom'] == nom_objet:
            # Vérifier que l'objet peut être vendu
            if objet['prix'] == 0:
                print("Cet objet ne peut pas être vendu")
                return False

            # Déséquiper l'objet s'il est porté
            if objet.get('porte', False):
                objet['porte'] = False

            prix_vente = objet['prix'] // 2
            personnage['pieces_or'] += prix_vente
            personnage['inventaire'].pop(i)
            print(f"{nom_objet} vendu pour {prix_vente} pièces d'or !")
            return True

    print("Objet non trouvé dans l'inventaire")
    return False

def afficher_inventaire(personnage):
    """Affiche l'inventaire du personnage"""
    print(f"\n=== INVENTAIRE DE {personnage['nom'].upper()} ===")
    print(f"Pièces d'or : {personnage['pieces_or']}")

    if not personnage['inventaire']:
        print("Inventaire vide")
        return

    equipés = [obj for obj in personnage['inventaire'] if obj.get('porte', False)]
    non_equipés = [obj for obj in personnage['inventaire'] if not obj.get('porte', False)]

    if equipés:
        print("\n--- OBJETS ÉQUIPÉS ---")
        for objet in equipés:
            stats_str = ""
            if objet['stats']:
                stats_list = []
                for stat, val in objet['stats'].items():
                    if val > 0:
                        stats_list.append(f"+{val} {stat}")
                    elif val < 0:
                        stats_list.append(f"{val} {stat}")
                if stats_list:
                    stats_str = f" ({', '.join(stats_list)})"
            print(f"  ⚔️ {objet['nom']} [{objet['slot']}]{stats_str}")

    if non_equipés:
        print("\n--- OBJETS NON ÉQUIPÉS ---")
        for i, objet in enumerate(non_equipés, 1):
            print(f"  {i}. {objet['nom']} - {objet['prix']} po ({objet['type']})")

def menu_boutique(personnage):
    """Menu de la boutique"""
    if personnage is None:
        print("Vous devez d'abord créer ou charger un personnage !")
        return

    # Vérifier si le personnage est mort
    if personnage['points_de_vie_actuels'] <= 0:
        print(f"\n💀 {personnage['nom']} est mort ! 💀")
        print("Un personnage mort ne peut pas faire d'achats.")
        print("Veuillez créer un nouveau personnage ou en charger un autre.")
        input("Appuyez sur Entrée pour retourner au menu principal...")
        return

    while True:
        print(f"\n=== BOUTIQUE D'ÉQUIPEMENT ===")
        print(f"Argent disponible : {personnage['pieces_or']} pièces d'or")
        print("1. Voir les objets à vendre")
        print("2. Acheter un objet")
        print("3. Vendre un objet")
        print("4. Retour au menu principal")

        choix = input("Votre choix (1-4) : ")

        if choix == "1":
            boutique = charger_boutique()
            if boutique:
                print(f"\n=== OBJETS DISPONIBLES ({len(boutique)}) ===")
                for i, objet in enumerate(boutique, 1):
                    print(f"{i}. {objet['nom']} - {objet['prix']} po")

                try:
                    num = int(input("\nTapez le numéro d'un objet pour voir ses détails (0 pour annuler) : "))
                    if 1 <= num <= len(boutique):
                        afficher_objet(boutique[num-1])
                except ValueError:
                    print("Numéro invalide")

        elif choix == "2":
            boutique = charger_boutique()
            if boutique:
                print(f"\n=== ACHETER UN OBJET ===")
                for i, objet in enumerate(boutique, 1):
                    print(f"{i}. {objet['nom']} - {objet['prix']} po")

                try:
                    num = int(input("\nNuméro de l'objet à acheter (0 pour annuler) : "))
                    if 1 <= num <= len(boutique):
                        acheter_objet(personnage, boutique[num-1])
                except ValueError:
                    print("Numéro invalide")

        elif choix == "3":
            if personnage['inventaire']:
                print(f"\n=== VENDRE UN OBJET ===")
                objets_vendables = [obj for obj in personnage['inventaire'] if obj['prix'] > 0]

                if objets_vendables:
                    for i, objet in enumerate(objets_vendables, 1):
                        prix_vente = objet['prix'] // 2
                        equipe = " (équipé)" if objet.get('porte', False) else ""
                        print(f"{i}. {objet['nom']} - {prix_vente} po{equipe}")

                    try:
                        num = int(input("\nNuméro de l'objet à vendre (0 pour annuler) : "))
                        if 1 <= num <= len(objets_vendables):
                            vendre_objet(personnage, objets_vendables[num-1]['nom'])
                    except ValueError:
                        print("Numéro invalide")
                else:
                    print("Aucun objet vendable dans votre inventaire")
            else:
                print("Votre inventaire est vide")

        elif choix == "4":
            break

        else:
            print("Choix invalide")

def menu_inventaire(personnage):
    """Menu de gestion de l'inventaire"""
    if personnage is None:
        print("Vous devez d'abord créer ou charger un personnage !")
        return

    # Vérifier si le personnage est mort
    if personnage['points_de_vie_actuels'] <= 0:
        print(f"\n💀 {personnage['nom']} est mort ! 💀")
        print("Un personnage mort ne peut pas gérer son inventaire.")
        print("Veuillez créer un nouveau personnage ou en charger un autre.")
        input("Appuyez sur Entrée pour retourner au menu principal...")
        return

    while True:
        afficher_inventaire(personnage)
        print("\n1. Équiper un objet")
        print("2. Déséquiper un objet")
        print("3. Retour au menu principal")

        choix = input("Votre choix (1-3) : ")

        if choix == "1":
            objets_non_equipes = [obj for obj in personnage['inventaire'] if not obj.get('porte', False) and obj['slot'] != "aucun"]
            if objets_non_equipes:
                print("\nObjets à équiper :")
                for i, objet in enumerate(objets_non_equipes, 1):
                    print(f"{i}. {objet['nom']} [{objet['slot']}]")

                try:
                    num = int(input("Numéro de l'objet à équiper (0 pour annuler) : "))
                    if 1 <= num <= len(objets_non_equipes):
                        equiper_objet(personnage, objets_non_equipes[num-1]['nom'])
                except ValueError:
                    print("Numéro invalide")
            else:
                print("Aucun objet à équiper")

        elif choix == "2":
            objets_equipes = [obj for obj in personnage['inventaire'] if obj.get('porte', False)]
            if objets_equipes:
                print("\nObjets équipés :")
                for i, objet in enumerate(objets_equipes, 1):
                    print(f"{i}. {objet['nom']} [{objet['slot']}]")

                try:
                    num = int(input("Numéro de l'objet à déséquiper (0 pour annuler) : "))
                    if 1 <= num <= len(objets_equipes):
                        desequiper_objet(personnage, objets_equipes[num-1]['nom'])
                except ValueError:
                    print("Numéro invalide")
            else:
                print("Aucun objet équipé")

        elif choix == "3":
            break

        else:
            print("Choix invalide")

# ===============================================
# SECTION 5: FONCTIONS MONSTRES
# ===============================================

def charger_monstres():
    """Charge la base de données des monstres depuis le fichier JSON"""
    try:
        with open('monstres.json', 'r', encoding='utf-8') as fichier:
            monstres = json.load(fichier)
        print(f"Base de données chargée : {len(monstres)} monstres trouvés")
        return monstres
    except FileNotFoundError:
        print("Erreur : Le fichier monstres.json n'a pas été trouvé")
        return []
    except json.JSONDecodeError:
        print("Erreur : Le fichier JSON est mal formaté")
        return []

def afficher_monstre(monstre):
    """Affiche les détails d'un monstre"""
    print(f"\n=== {monstre['nom']} ===")
    print(f"Points de vie : {monstre['pvies']}")
    print(f"Initiative : {monstre['initiative']}")
    print(f"Element : {monstre['element']}")
    print(f"Attaques :")
    print(f"  1. {monstre['attaque1']}")
    if monstre.get('attaque2'):
        print(f"  2. {monstre['attaque2']}")
    if monstre.get('attaque3'):
        print(f"  3. {monstre['attaque3']}")
    print(f"Pieces d'or : {monstre['pieces_or']}")
    print(f"Points d'experience : {monstre['pts_experience']}")
    if monstre.get('capturable'):
        print("Capturable : Oui")
    else:
        print("Capturable : Non")

def lister_monstres():
    """Affiche la liste de tous les monstres"""
    monstres = charger_monstres()
    if not monstres:
        return

    print("\n=== LISTE DES MONSTRES ===")
    for i, monstre in enumerate(monstres, 1):
        print(f"{i}. {monstre['nom']} (PV: {monstre['pvies']}, Element: {monstre['element']})")

def chercher_monstre_par_nom(nom):
    """Cherche un monstre par son nom"""
    monstres = charger_monstres()
    for monstre in monstres:
        if monstre['nom'].lower() == nom.lower():
            return monstre
    return None

def filtrer_monstres_par_element(element):
    """Filtre les monstres par élément"""
    monstres = charger_monstres()
    monstres_filtres = []
    for monstre in monstres:
        if monstre['element'].lower() == element.lower():
            monstres_filtres.append(monstre)
    return monstres_filtres

def menu_monstres():
    """Menu pour explorer la base de données des monstres"""
    while True:
        print("\n=== BASE DE DONNEES DES MONSTRES ===")
        print("1. Lister tous les monstres")
        print("2. Chercher un monstre par nom")
        print("3. Filtrer par element")
        print("4. Retour au menu principal")

        choix = input("Votre choix (1-4) : ")

        if choix == "1":
            lister_monstres()
            monstres = charger_monstres()
            if monstres:
                try:
                    num = int(input("\nTapez le numéro d'un monstre pour voir ses détails (0 pour annuler) : "))
                    if 1 <= num <= len(monstres):
                        afficher_monstre(monstres[num-1])
                except ValueError:
                    print("Numéro invalide")

        elif choix == "2":
            nom = input("Nom du monstre à chercher : ")
            monstre = chercher_monstre_par_nom(nom)
            if monstre:
                afficher_monstre(monstre)
            else:
                print(f"Aucun monstre trouvé avec le nom '{nom}'")

        elif choix == "3":
            element = input("Element à filtrer (Feu, Nature, Eau, Electricite, Lumiere, Obscurite, Bien, Mal, Terre) : ")
            monstres_filtres = filtrer_monstres_par_element(element)
            if monstres_filtres:
                print(f"\nMonstres de l'element {element} :")
                for monstre in monstres_filtres:
                    print(f"- {monstre['nom']} (PV: {monstre['pvies']})")
            else:
                print(f"Aucun monstre trouvé pour l'element '{element}'")

        elif choix == "4":
            break

        else:
            print("Choix invalide")

# ===============================================
# SECTION 6: FONCTIONS MISSIONS
# ===============================================

def charger_missions():
    """Charge la base de données des missions depuis le fichier JSON"""
    try:
        with open('missions.json', 'r', encoding='utf-8') as fichier:
            missions = json.load(fichier)
        return missions
    except FileNotFoundError:
        print("Erreur : Le fichier missions.json n'a pas été trouvé")
        return []
    except json.JSONDecodeError:
        print("Erreur : Le fichier missions.json est mal formaté")
        return []

def missions_disponibles(personnage):
    """Retourne les missions disponibles pour un personnage"""
    missions = charger_missions()
    missions_dispo = []

    for mission in missions:
        # Vérifier si le personnage peut faire cette mission
        classe_ok = (mission['classe'] == 'tous' or mission['classe'] == personnage['classe'])
        niveau_ok = personnage['experience'] >= mission['niveauxp']
        pas_faite = not mission['faite'] or mission['repetable']

        if classe_ok and niveau_ok and pas_faite:
            missions_dispo.append(mission)

    return missions_dispo

def afficher_mission(mission):
    """Affiche les détails d'une mission"""
    print(f"\n=== {mission['nom']} ===")
    print(f"Description : {mission['description']}")
    print(f"Classe requise : {mission['classe']}")
    print(f"Expérience requise : {mission['niveauxp']} XP")
    print(f"Récompenses :")
    print(f"  - Expérience : +{mission['xpwin']} XP")
    print(f"  - Or : +{mission['orwin']} pièces")
    print(f"Ennemi(s) : {mission['monstrenombre']} {mission['monstremission']}")
    if mission['repetable']:
        print("Mission répétable : Oui")
    else:
        print("Mission répétable : Non")
    if mission['faite']:
        print("Statut : Terminée")
    else:
        print("Statut : Disponible")

def afficher_missions_par_page(missions, page=1, missions_par_page=10):
    """Affiche les missions avec pagination"""
    total_pages = (len(missions) + missions_par_page - 1) // missions_par_page
    debut = (page - 1) * missions_par_page
    fin = min(debut + missions_par_page, len(missions))

    missions_page = missions[debut:fin]

    print(f"\n=== PAGE {page}/{total_pages} ({len(missions)} missions au total) ===")
    for i, mission in enumerate(missions_page, debut + 1):
        print(f"{i}. {mission['nom']} (XP: +{mission['xpwin']}, Or: +{mission['orwin']})")

    return missions_page, total_pages

def repos(personnage):
    """Permet au personnage de se reposer pour récupérer ses PV"""
    # Vérifier si le personnage est mort
    if personnage['points_de_vie_actuels'] <= 0:
        print("💀 Un personnage mort ne peut pas se reposer ! Il est définitivement mort.")
        return

    stats_base = calculer_stats_personnage(personnage)
    pv_max = stats_base['pv']
    pv_recupere = pv_max - personnage['points_de_vie_actuels']

    if pv_recupere <= 0:
        print("Vous êtes déjà au maximum de vos points de vie.")
        return

    personnage['points_de_vie_actuels'] = pv_max
    print(f"Vous vous reposez et récupérez {pv_recupere} points de vie.")
    print(f"Vos points de vie actuels sont maintenant : {personnage['points_de_vie_actuels']}/{pv_max}")
    
    # Sauvegarder après le repos
    sauvegarder_personnage(personnage)
    print("✅ Progression sauvegardée")

def commencer_combat(personnage, mission):
    """Lance le combat pour une mission donnée"""
    print(f"\n=== DÉBUT DU COMBAT - {mission['nom']} ===")
    print(f"Vous devez affronter {mission['monstrenombre']} {mission['monstremission']}")

    # Charger les données du monstre
    monstres = charger_monstres()
    monstre_template = None
    for m in monstres:
        if m['nom'] == mission['monstremission']:
            monstre_template = m
            break

    if not monstre_template:
        print("Erreur: Monstre non trouvé dans la base de données!")
        return False

    # Calculer les stats du personnage
    stats_personnage = calculer_stats_personnage(personnage)

    print(f"\n=== VOS STATISTIQUES ===")
    # Utiliser les points de vie actuels du personnage
    print(f"Points de vie: {personnage['points_de_vie_actuels']}/{stats_personnage['pv']}")
    print(f"Attaque: {stats_personnage['attaque']}")
    print(f"Défense: {stats_personnage['defense']}")

    # Créer plusieurs instances des monstres
    monstres_combat = []
    for i in range(mission['monstrenombre']):
        monstre_copie = monstre_template.copy()
        monstre_copie['nom'] = f"{monstre_template['nom']}{i+1}"
        monstre_copie['vivant'] = True
        # Utiliser les PV du monstre du template
        monstre_copie['pvies'] = monstre_template['pvies']
        monstres_combat.append(monstre_copie)

    print(f"\n=== MONSTRES À AFFRONTER ===")
    for i, monstre in enumerate(monstres_combat):
        print(f"{i+1}. {monstre['nom']} (PV: {monstre['pvies']})")

    # Combat tour par tour
    pv_personnage = personnage['points_de_vie_actuels'] # Initialiser avec les PV actuels
    monstres_vivants = len(monstres_combat)
    tour = 1

    while pv_personnage > 0 and monstres_vivants > 0:
        print(f"\n=== TOUR {tour} ===")
        print(f"Vos PV: {pv_personnage}")

        # Afficher les monstres vivants
        print("Monstres encore en vie:")
        monstres_actifs = []
        for i, monstre in enumerate(monstres_combat):
            if monstre['vivant']:
                monstres_actifs.append((i, monstre))
                print(f"  {len(monstres_actifs)}. {monstre['nom']} (PV: {monstre['pvies']})")

        # Le joueur choisit sa cible
        if len(monstres_actifs) > 1:
            try:
                choix = int(input(f"Choisissez votre cible (1-{len(monstres_actifs)}) : "))
                if 1 <= choix <= len(monstres_actifs):
                    cible_index, cible = monstres_actifs[choix-1]
                else:
                    print("Choix invalide, attaque le premier monstre disponible")
                    cible_index, cible = monstres_actifs[0]
            except ValueError:
                print("Choix invalide, attaque le premier monstre disponible")
                cible_index, cible = monstres_actifs[0]
        else:
            cible_index, cible = monstres_actifs[0]

        # Attaque du personnage
        degats_perso = max(1, stats_personnage['attaque'] - random.randint(0, 2))
        cible['pvies'] -= degats_perso
        print(f"\nVous attaquez {cible['nom']} et infligez {degats_perso} dégâts !")

        if cible['pvies'] <= 0:
            print(f"💀 {cible['nom']} est vaincu !")
            cible['vivant'] = False
            monstres_vivants -= 1

            if monstres_vivants == 0:
                break
        else:
            print(f"{cible['nom']} a encore {cible['pvies']} PV")

        # Attaque des monstres survivants
        for monstre in monstres_combat:
            if monstre['vivant']:
                degats_monstre = max(1, random.randint(2, 6) - (stats_personnage['defense'] // 2))
                pv_personnage -= degats_monstre
                print(f"{monstre['nom']} vous attaque et inflige {degats_monstre} dégâts !")

                if pv_personnage <= 0:
                    break

        if pv_personnage <= 0:
            break

        tour += 1

        # Éviter les combats infiniment longs
        if tour > 30:
            print("Le combat s'éternise... Les monstres fuient!")
            monstres_vivants = 0
            break

    # Résultats
    if monstres_vivants == 0 and pv_personnage > 0:
        print(f"\n🎉 MISSION RÉUSSIE ! 🎉")
        print(f"Vous avez vaincu tous les {mission['monstremission']} !")

        # Distribuer les récompenses
        personnage['experience'] += mission['xpwin']
        personnage['pieces_or'] += mission['orwin']

        print(f"Récompenses obtenues:")
        print(f"  +{mission['xpwin']} XP (Total: {personnage['experience']})")
        print(f"  +{mission['orwin']} pièces d'or (Total: {personnage['pieces_or']})")

        # Mettre à jour les PV actuels du personnage
        personnage['points_de_vie_actuels'] = pv_personnage

        # Marquer la mission comme faite si elle n'est pas répétable
        if not mission['repetable']:
            mission['faite'] = True
            # Sauvegarder les changements dans le fichier missions.json
            missions = charger_missions()
            for m in missions:
                if m['nom'] == mission['nom']:
                    m['faite'] = True
                    break
            try:
                with open('missions.json', 'w', encoding='utf-8') as fichier:
                    json.dump(missions, fichier, indent=2, ensure_ascii=False)
            except Exception as e:
                print(f"Erreur lors de la sauvegarde des missions: {e}")

        return True
    else:
        print(f"\n💀 MISSION ÉCHOUÉE 💀")
        monstres_vaincus = mission['monstrenombre'] - monstres_vivants
        print(f"Vous avez vaincu {monstres_vaincus}/{mission['monstrenombre']} monstres avant d'être défait")
        # Mettre à jour les PV actuels du personnage même en cas d'échec
        personnage['points_de_vie_actuels'] = pv_personnage
        return False

def calculer_stats_personnage(personnage):
    """Calcule les statistiques de combat du personnage"""
    # Stats de base
    force = personnage['attributs']['Force']
    endurance = personnage['attributs']['Endurance']
    habilete = personnage['attributs']['Habileté']

    stats = {
        'pv': 10 + (endurance * 3),
        'attaque': 5 + force,
        'defense': 2 + (endurance // 2)
    }

    # Bonus d'équipement
    for objet in personnage['inventaire']:
        if objet.get('porte', False) and 'stats' in objet:
            for stat, valeur in objet['stats'].items():
                if stat == 'degats':
                    stats['attaque'] += valeur
                elif stat == 'defense':
                    stats['defense'] += valeur

    return stats

def simuler_combat_simple(personnage_stats, monstre):
    """Simule un combat simple entre le personnage et un monstre"""
    pv_personnage = personnage_stats['pv']
    pv_monstre = monstre['pvies']

    print(f"Combat: {pv_personnage} PV vs {monstre['nom']} ({pv_monstre} PV)")

    tour = 1
    while pv_personnage > 0 and pv_monstre > 0:
        print(f"\n--- Tour {tour} ---")

        # Attaque du personnage
        degats_perso = max(1, personnage_stats['attaque'] - random.randint(0, 2))
        pv_monstre -= degats_perso
        print(f"Vous infligez {degats_perso} dégâts au {monstre['nom']} (PV: {max(0, pv_monstre)})")

        if pv_monstre <= 0:
            return True

        # Attaque du monstre
        degats_monstre = max(1, random.randint(2, 6) - (personnage_stats['defense'] // 2))
        pv_personnage -= degats_monstre
        print(f"Le {monstre['nom']} vous inflige {degats_monstre} dégâts (PV: {max(0, pv_personnage)})")

        tour += 1

        # Éviter les combats infiniment longs
        if tour > 20:
            print("Le combat s'éternise... Match nul!")
            return random.choice([True, False])

    return False

def menu_missions(personnage):
    """Menu pour explorer les missions"""
    if personnage is None:
        print("Vous devez d'abord créer ou charger un personnage !")
        return

    # Vérifier si le personnage est mort
    if personnage['points_de_vie_actuels'] <= 0:
        print(f"\n💀 {personnage['nom']} est mort ! 💀")
        print("Vous ne pouvez pas faire de missions avec un personnage mort.")
        print("Veuillez créer un nouveau personnage ou en charger un autre.")
        input("Appuyez sur Entrée pour retourner au menu principal...")
        return

    while True:
        print(f"\n=== MISSIONS POUR {personnage['nom']} ===")
        print(f"Classe: {personnage['classe']} | Expérience: {personnage['experience']} XP")
        print("1. Voir missions disponibles")
        print("2. Voir toutes les missions")
        print("3. Repos (Récupérer PV)")
        print("4. Retour au menu principal")

        choix = input("Votre choix (1-4) : ")

        if choix == "1":
            missions_dispo = missions_disponibles(personnage)
            if missions_dispo:
                page = 1
                while True:
                    missions_page, total_pages = afficher_missions_par_page(missions_dispo, page)

                    print(f"\nOptions: [N]uméro mission, [P]age suivante, [R]etour, [C]ombat")
                    if page > 1:
                        print("         [A]rrière (page précédente)")

                    choix_mission = input("Votre choix : ").lower()

                    if choix_mission == 'r':
                        break
                    elif choix_mission == 'p' and page < total_pages:
                        page += 1
                    elif choix_mission == 'a' and page > 1:
                        page -= 1
                    elif choix_mission == 'c':
                        try:
                            num = int(input("Numéro de la mission à combattre : "))
                            if 1 <= num <= len(missions_dispo):
                                mission_choisie = missions_dispo[num-1]
                                print(f"\n=== {mission_choisie['nom']} ===")
                                afficher_mission(mission_choisie)

                                confirmer = input("\nCommencer le combat ? (o/n) : ")
                                if confirmer.lower() in ['o', 'oui', 'y', 'yes']:
                                    if commencer_combat(personnage, mission_choisie):
                                        # Combat réussi - sauvegarder automatiquement
                                        sauvegarder_personnage(personnage)
                                        print("✅ Progression sauvegardée automatiquement")
                                    else:
                                        # Combat échoué - sauvegarder aussi pour éviter la triche
                                        sauvegarder_personnage(personnage)
                                        print("💾 État du personnage sauvegardé")
                                        
                                        # Vérifier si le personnage est mort
                                        if personnage['points_de_vie_actuels'] <= 0:
                                            print("\n💀 VOTRE PERSONNAGE EST MORT ! 💀")
                                            print("Vous ne pouvez plus jouer avec ce personnage.")
                                            print("Vous devez créer un nouveau personnage ou en charger un autre.")
                                            input("Appuyez sur Entrée pour continuer...")
                                            return

                            else:
                                print("Numéro invalide")
                        except ValueError:
                            print("Numéro invalide")
                    elif choix_mission.isdigit():
                        num = int(choix_mission)
                        if 1 <= num <= len(missions_dispo):
                            afficher_mission(missions_dispo[num-1])
                        else:
                            print("Numéro invalide")
                    else:
                        print("Choix invalide")
            else:
                print("\nAucune mission disponible pour votre personnage.")
                print("Vous devez peut-être gagner plus d'expérience ou changer de classe.")

        elif choix == "2":
            missions = charger_missions()
            if missions:
                page = 1
                while True:
                    print(f"\n=== TOUTES LES MISSIONS - PAGE {page} ===")
                    debut = (page - 1) * 10
                    fin = min(debut + 10, len(missions))
                    total_pages = (len(missions) + 9) // 10

                    for i in range(debut, fin):
                        mission = missions[i]
                        statut = "✓" if mission['faite'] else "○"
                        classe_ok = "✓" if (mission['classe'] == 'tous' or mission['classe'] == personnage['classe']) else "✗"
                        niveau_ok = "✓" if personnage['experience'] >= mission['niveauxp'] else "✗"
                        print(f"{i+1}. {statut} {mission['nom']} [Classe:{classe_ok} Niveau:{niveau_ok}]")

                    print(f"\nPage {page}/{total_pages}")
                    choix_page = input("Tapez un numéro, 'p' (suivant), 'a' (arrière) ou 'r' (retour) : ").lower()

                    if choix_page == 'r':
                        break
                    elif choix_page == 'p' and page < total_pages:
                        page += 1
                    elif choix_page == 'a' and page > 1:
                        page -= 1
                    elif choix_page.isdigit():
                        num = int(choix_page)
                        if 1 <= num <= len(missions):
                            afficher_mission(missions[num-1])

        elif choix == "3":
            repos(personnage)

        elif choix == "4":
            break

        else:
            print("Choix invalide")

# ===============================================
# SECTION 7: FONCTIONS ATTAQUES
# ===============================================

def charger_attaques():
    """Charge la base de données des attaques depuis le fichier JSON"""
    try:
        with open('attaques.json', 'r', encoding='utf-8') as fichier:
            attaques = json.load(fichier)
        return attaques
    except FileNotFoundError:
        print("Erreur : Le fichier attaques.json n'a pas été trouvé")
        return []
    except json.JSONDecodeError:
        print("Erreur : Le fichier attaques.json est mal formaté")
        return []

def afficher_attaque(attaque):
    """Affiche les détails d'une attaque"""
    print(f"\n=== {attaque['nom']} ===")
    print(f"Type : {attaque['type']}")
    print(f"Dégâts : {attaque['degats']}")
    print(f"Précision : {attaque['precision']}%")
    print(f"Élément : {attaque['element']}")
    print(f"Description : {attaque['description']}")
    if attaque.get('effet'):
        print(f"Effet spécial : {attaque['effet']}")

def lister_attaques():
    """Affiche la liste de toutes les attaques"""
    attaques = charger_attaques()
    if not attaques:
        return

    print("\n=== LISTE DES ATTAQUES ===")
    for i, attaque in enumerate(attaques, 1):
        print(f"{i}. {attaque['nom']} ({attaque['type']}) - {attaque['degats']} dégâts")

def chercher_attaque_par_nom(nom):
    """Cherche une attaque par son nom"""
    attaques = charger_attaques()
    for attaque in attaques:
        if attaque['nom'].lower() == nom.lower():
            return attaque
    return None

def filtrer_attaques_par_type(type_attaque):
    """Filtre les attaques par type"""
    attaques = charger_attaques()
    attaques_filtrees = []
    for attaque in attaques:
        if attaque['type'].lower() == type_attaque.lower():
            attaques_filtrees.append(attaque)
    return attaques_filtrees

def menu_attaques():
    """Menu pour explorer la base de données des attaques"""
    while True:
        print("\n=== BASE DE DONNEES DES ATTAQUES ===")
        print("1. Lister toutes les attaques")
        print("2. Chercher une attaque par nom")
        print("3. Filtrer par type")
        print("4. Retour au menu principal")

        choix = input("Votre choix (1-4) : ")

        if choix == "1":
            lister_attaques()
            attaques = charger_attaques()
            if attaques:
                try:
                    num = int(input("\nTapez le numéro d'une attaque pour voir ses détails (0 pour annuler) : "))
                    if 1 <= num <= len(attaques):
                        afficher_attaque(attaques[num-1])
                except ValueError:
                    print("Numéro invalide")

        elif choix == "2":
            nom = input("Nom de l'attaque à chercher : ")
            attaque = chercher_attaque_par_nom(nom)
            if attaque:
                afficher_attaque(attaque)
            else:
                print(f"Aucune attaque trouvée avec le nom '{nom}'")

        elif choix == "3":
            type_att = input("Type à filtrer (Physique, Magique, Distance, Soin, Buff, Controle, Poison) : ")
            attaques_filtrees = filtrer_attaques_par_type(type_att)
            if attaques_filtrees:
                print(f"\nAttaques de type {type_att} :")
                for attaque in attaques_filtrees:
                    print(f"- {attaque['nom']} ({attaque['degats']} dégâts)")
            else:
                print(f"Aucune attaque trouvée pour le type '{type_att}'")

        elif choix == "4":
            break

        else:
            print("Choix invalide")

# ===============================================
# SECTION 8: PROGRAMME PRINCIPAL ET MENUS
# ===============================================

print("JEU DE ROLE - MENU PRINCIPAL\n")

personnage_actuel = None

while True:
    print("\n=== MENU PRINCIPAL ===")
    if personnage_actuel:
        print(f"Personnage actuel : {personnage_actuel['nom']} ({personnage_actuel['classe']}) - {personnage_actuel['experience']} XP")
    else:
        print("Aucun personnage chargé")

    print("1. Gestion des personnages")
    print("2. Missions")
    print("3. Boutique d'équipement")
    print("4. Inventaire")
    print("5. Explorer la base de donnees des monstres")
    print("6. Explorer la base de donnees des attaques")
    print("7. Quitter")

    choix_menu = input("Votre choix (1-7) : ")

    if choix_menu == "1":
        nouveau_personnage = menu_personnage()
        if nouveau_personnage:
            personnage_actuel = nouveau_personnage

    elif choix_menu == "2":
        menu_missions(personnage_actuel)

    elif choix_menu == "3":
        menu_boutique(personnage_actuel)

    elif choix_menu == "4":
        menu_inventaire(personnage_actuel)

    elif choix_menu == "5":
        menu_monstres()

    elif choix_menu == "6":
        menu_attaques()

    elif choix_menu == "7":
        if personnage_actuel:
            sauver = input("Voulez-vous sauvegarder votre personnage avant de quitter ? (o/n) : ")
            if sauver.lower() in ['o', 'oui', 'y', 'yes']:
                sauvegarder_personnage(personnage_actuel)
        print("Au revoir !")
        break

    else:
        print("Choix invalide")