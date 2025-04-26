import random
import nltk

nltk.download('punkt')

game = {
            "Japon": "Un pays insulaire d'Asie connu pour sa technologie avancée et sa culture unique, comme les samouraïs et les geishas.",
            "Canada": "Un grand pays d'Amérique du Nord avec des paysages magnifiques, des montagnes et des forêts.",
            "Russie": "Le plus grand pays du monde, traversant l'Europe et l'Asie, avec une histoire riche et des sites historiques.",
            "Brésil": "le plus grand pays d'Amérique du Sud, connu pour ses plages magnifiques, sa forêt amazonienne et sa culture vibrante",
            "Italie":"située en Europe du Sud, est célèbre pour son art, son architecture et sa cuisine",
            "Espagne":"située dans le sud-ouest de l'Europe, est célèbre pour sa culture vibrante, ses plages magnifiques et ses monuments historiques comme l'Alhambra et la Sagrada Família", 
}

def chatbot():
    print("bienvenue !")
    print("je vais vous donnez la description et vous devinez le jeu")
    
    
    jeu, description = random.choice(list(game.items()))  
    
    print("\nc'est la description :")
    print(description)
    
    
    while True:
        guess = input("\nQuel est le nom?").strip()

        if jeu.lower() == guess.lower():
            print(f"bravo!")
            break
        else:
           print("Désolé, essaie encore !")

# Lancer le chatbot
if __name__ == "__main__":
    while True:
        chatbot()
        play_again = input("\nVeux-tu jouer à nouveau ? (oui/non) ").strip().lower()
        if play_again != "oui":
            print("Merci d'avoir joué ! À bientôt.")
            break