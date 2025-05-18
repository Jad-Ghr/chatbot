import customtkinter as ctk
from appfun import predict_answer  # Import the prediction function
import pymongo
from datetime import datetime



myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["chatBot_Conversation"]

mycol = mydb["conversation"]


def get_current_date():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")



def send_mess(event=None):
    msg_dict = {}
    user_mess = user_input.get()
    current_time = get_current_date()
    if user_mess.strip() != "":
        chat_history.configure(state="normal")
        chat_history.insert("end", f"You:{user_mess}\n", "user")
        msg_dict["user"] = f"[{current_time}] You: {user_mess}\n"
        bot_reponse = predict_answer(user_mess)
        chat_history.insert("end", f"chatbot:{bot_reponse}\n", "bot")
        msg_dict["chatbot"] = f"[{current_time}] chatbot:{bot_reponse}\n"
        chat_history.configure(state="disabled")
        chat_history.see("end")
        user_input.delete(0, "end")
        try:
            mycol.insert_one(msg_dict)
        except Exception as e:
            print("MongoDB insert error:", e)

history_panel = None
history_visible = False

def toggle_history_panel():
    global history_panel, history_visible

    if history_visible:
        history_panel.destroy()
        history_panel = None
        history_visible = False
    else:
        history_panel = ctk.CTkFrame(app, width=300, fg_color="#1f1f2f")
        history_panel.place(x=0, y=0, relheight=1)

        # Add the close button inside the panel
        close_button = ctk.CTkButton(
            history_panel,
            text="📜",
            font=("Arial", 16, "bold"),
            width=40,
            height=40,
            corner_radius=10,
            command=toggle_history_panel  # Reuses the same function to hide
        )
        close_button.pack(side="left", anchor="n", padx=10, pady=10)

        history_text = ctk.CTkTextbox(history_panel, state="normal")
        history_text.pack(padx=10, pady=(0, 10), fill="both", expand=True)

        for doc in mycol.find():
            history_text.insert("end", doc["user"] + "\n", "user")
            history_text.insert("end", doc["chatbot"] + "\n\n", "bot")

        history_text.tag_config("user", foreground="#00ffff")
        history_text.tag_config("bot", foreground="#7CFC00")
        history_text.configure(state="disabled")

        history_visible = True



# ------ Interface ------

# Design settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.geometry("600x700")
app.title("🎮 Chatbot Gaming Zone 🎮")
app.configure(bg="#1e1e2f")

# En-tête avec trois points à gauche
header_frame = ctk.CTkFrame(app, fg_color="#1e1e2f", height=50)
header_frame.pack(fill="x", padx=15)

# Bouton de trois points à gauche (fixe à gauche du header)
three_dots_button = ctk.CTkButton(
    header_frame,
    text="📜",
    font=("Arial", 16, "bold"),
    width=40,
    height=40,
    corner_radius=10,
    command=toggle_history_panel  # Ouvre la fenêtre d'historique
)
three_dots_button.pack(side="left", padx=10, pady=10)  # Bouton "⋮" à gauche, visible toujours

# Titre (à gauche) et bouton trois points (à droite)
header = ctk.CTkLabel(
    header_frame,
    text="👾 Bienvenue sur le Chatbot Gaming Zone 👾",
    font=("Comic Sans MS", 20, "bold"),
    text_color="#00f2ff",
)
header.pack(side="left", padx=10, pady=10, anchor="w")  # Titre à gauche sans occuper toute la largeur

# Zone d'affichage de l'historique
chat_history = ctk.CTkTextbox(
    app,
    height=550,
    fg_color="#282c34",
    text_color="#ffffff",
    corner_radius=12,
    state="disabled",
    border_color="#00f2ff",
    border_width=1,
    font=("Consolas", 16),
)
chat_history.tag_config("user", foreground="#00ffff")
chat_history.tag_config("bot", foreground="#7CFC00")
chat_history.pack(pady=10, padx=15, fill="both", expand=True)

# Cadre de saisie utilisateur et bouton sur la même ligne
user_input_frame = ctk.CTkFrame(
    app,
    fg_color="#2b2b40",
    corner_radius=10
)
user_input_frame.pack(pady=10, padx=15, fill="x")

# Zone de saisie avec CTkEntry (utilisation d'Entry pour un texte à ligne unique)
user_input = ctk.CTkEntry(  # Utilisation de CTkEntry pour la saisie de texte simple
    user_input_frame,
    height=50,
    font=("Verdana", 14),
    corner_radius=10,
    border_color="#00f2ff",
    border_width=3,
    fg_color="#1e1e2f",
    text_color="#ffffff",
)
user_input.pack(side="left", padx=10, pady=10, fill="both", expand=True)  # Zone de saisie à gauche

# Bouton envoyer à droite
send_button = ctk.CTkButton(
    user_input_frame,
    text="Envoyer 🚀",
    font=("Arial", 14, "bold"),
    width=120,
    height=40,
    corner_radius=10,
    command=send_mess
)
send_button.pack(side="right", padx=10, pady=10)  # Bouton "Envoyer" à droite

# Gérer touche Entrée
app.bind("<Return>", send_mess)

# Lancer l'application
app.mainloop()