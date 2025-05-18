import nltk
from nltk.tokenize import word_tokenize
import random

# Ensure NLTK resources are available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')



# Base de connaissances simple
def les_reponses(lentree):
    salutations = [
        "Salut ! Est-ce que tu as joué à un jeu récemment ?",
        "Salut ! Pourquoi hier tu n'as pas joué avec nous ?",
        "Yo ! T'as testé un nouveau jeu ?",
        "Hey ! T'as passé une bonne session de jeu ?"
    ]

    jeux_reponses = {
        "league of legends": [
            "LoL ? Mid ou top ?",
            "Quel champion tu joues le plus ?",
            "T'as fait un pentakill récemment ?"
        ],
        "fifa": [
            "FIFA ! PSG ou Real Madrid ?",
            "Tu préfères FUT ou Carrière ?",
            "Tu joues contre des potes ?"
        ],
        "gta": [
            "GTA, la liberté totale ! Tu préfères les missions ou le chaos ?",
            "Tu joues en ligne ou solo ?",
            "T'as déjà fait un braquage ?"
        ],
        "valorant": [
            "Valorant ! Tu joues quel agent ?",
            "T'as eu combien de kills cette partie ?",
            "Tu préfères jouer attaque ou défense ?"
        ],
        "minecraft": [
            "Ah Minecraft, un classique ! Tu joues en solo ou en multi ?",
            "Trop bien Minecraft ! Tu construis ou tu mines surtout ?",
            "Mode créatif ou survie ?"
        ],
        "fortnite": [
            "Fortnite ! Tu préfères le mode battle royale ou créatif ?",
            "Trop stylé ! Une victoire royale récemment ?",
            "Tu joues souvent avec ton squad ?"
        ],
        "apex": [
            "Apex Legends ? Tu joues qui ?",
            "Tu gères bien les tirs ?",
            "T’as déjà été champion ?"
        ],
        "csgo": [
            "CS:GO ! AK ou M4 ?",
            "Tu préfères Dust II ou Mirage ?",
            "Headshot facile ?"
        ],
        "roblox": [
            "Roblox, trop de choix de jeux ! Tu joues à quoi ?",
            "Tu crées aussi tes propres maps ?",
            "T'as des jeux favoris sur Roblox ?"
        ],
        "among us": [
            "T'es imposteur ou crewmate ?",
            "Trop marrant de piéger les autres !",
            "Tu joues avec des potes ou en ligne ?"
        ],
        "call of duty": [
            "Call of Duty ! Tu joues à Warzone ?",
            "Quel est ton mode préféré ?",
            "T’as fait beaucoup de kills récemment ?"
        ],
        "rocket league": [
            "Rocket League ! Buts aériens ?",
            "Tu joues en 2v2 ou 3v3 ?",
            "C'est un mélange fou entre foot et voitures !"
        ],
        "pubg": [
            "PUBG ! Un bon vieux battle royale.",
            "Tu préfères la version mobile ou PC ?",
            "T'as fait un top 1 récemment ?"
        ],
        "overwatch": [
            "Overwatch ! Quel est ton héros préféré ?",
            "Tu joues en attaque ou en soutien ?",
            "Tu préfères Overwatch 1 ou 2 ?"
        ],
        "the sims": [
            "The Sims ! Tu passes combien de temps à créer ta maison ?",
            "Tu fais souffrir tes Sims ? 😅",
            "Tu joues quel style de famille ?"
        ],
        "elden ring": [
            "Elden Ring ! Tu survis bien contre les boss ?",
            "C’est pas facile hein ?",
            "Tu joues magie ou corps-à-corps ?"
        ],
        "zelda": [
            "Zelda ! Tu préfères Breath of the Wild ou Tears of the Kingdom ?",
            "Tu explores tout ou tu fonces sur la quête ?",
            "Link est toujours prêt à sauver Hyrule !"
        ],
        "pokemon": [
            "Quel est ton starter préféré ?",
            "Tu vises tous les badges ?",
            "Tu joues à quelle version ?"
        ],
        "god of war": [
            "God of War ! Kratos est trop badass.",
            "Tu préfères les combats ou l'histoire ?",
            "Tu joues sur PS4 ou PS5 ?"
        ],
        "hollow knight": [
            "Hollow Knight est magnifique ! Tu galères avec les boss ?",
            "C’est dur mais tellement bon.",
            "Exploration à fond ?"
        ],
        "cyberpunk": [
            "Cyberpunk 2077 ! T'as aimé l'univers ?",
            "Tu joues quel style de personnage ?",
            "Trop stylé la customisation non ?"
        ],
        "red dead": [
            "Red Dead Redemption 2 ! Tu préfères les chevaux ou les duels ?",
            "T’as fini l’histoire ?",
            "La map est incroyable non ?"
        ],
        "terraria": [
            "Terraria ! Tu préfères miner ou combattre des boss ?",
            "Tu joues en solo ou avec des amis ?",
            "Tu l’as comparé à Minecraft ?"
        ],
        "fall guys": [
            "Fall Guys ! T’es bon aux mini-jeux ?",
            "Tu gagnes souvent ?",
            "Tu joues pour t’amuser ou pour gagner ?"
        ],
        "stardew valley": [
            "Stardew Valley ! Tu gères bien ta ferme ?",
            "Tu es plus pêche ou culture ?",
            "Tu joues en coop ?"
        ],
        "tetris": [
            "Tetris, un classique ! Tu arrives à aller loin ?",
            "Tu fais souvent des Tetrises ?",
            "Tu joues en mode rapide ou tranquille ?"
        ]
    }

    lentree_lower = lentree.lower()

    for jeu, reponses in jeux_reponses.items():
        if jeu in lentree_lower:
            return random.choice(reponses)

    if "bonjour" in lentree_lower or "salut" in lentree_lower:
        return random.choice(salutations)
    elif "comment" in lentree_lower and "ca" in lentree_lower:
        return "Je vais bien, merci de demander ! Et toi ?"
    elif "aide" in lentree_lower:
        return "Bien sûr ! Je suis là pour t'aider. Pose-moi une question."
    elif "merci" in lentree_lower:
        return "Avec plaisir !"
    elif "bye" in lentree_lower or "au revoir" in lentree_lower:
        return "À bientôt !"
    else:
        return "Je n'ai pas compris... peux-tu reformuler ?"

