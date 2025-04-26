import customtkinter as ctk
from appfun import predict_answer  # Import the prediction function




def send_mess(event=None):
    user_mess=user_input.get()
    if user_mess.strip()!="":
        chat_history.configure(state="normal")
        chat_history.insert("end",f"You:{user_mess}\n","user")
        bot_reponse=predict_answer(user_mess)
        chat_history.insert("end",f"chatbot:{bot_reponse}\n","bot")
        chat_history.configure(state="disabled")
        chat_history.see("end")
        user_input.delete(0,"end")
# Créer une instance de la fenêtre avec CustomTkinter
app = ctk.CTk()  

app.geometry("400x500")  
app.title("Chatbot Project")

# En-tête
header = ctk.CTkLabel(app, text="Welcome to ower chatbot project !", font=("Arial", 20, "bold"))
header.pack(pady=10)
#zone d'affichage les mess
chat_history = ctk.CTkTextbox(app,height=300,state="disabled")
chat_history.tag_config("user",foreground="black")
chat_history.tag_config("bot",foreground="blue")
chat_history.pack(pady=10,padx=10,fill="both",expand=True )
#champ de saisie utulisateur
user_input_frame = ctk.CTkFrame(app)
user_input_frame.pack(pady=10 ,padx=10,fill="x")

user_input=ctk.CTkEntry(user_input_frame,placeholder_text="Enter in her ...",width=275)
user_input.pack(side="left",padx=5)

send_button = ctk.CTkButton(user_input_frame,text="Send" ,command=send_mess)
send_button.pack(side="left")
#assurer la touche entre au champ de saisie pour envoyer le mess
app.bind("<Return>",send_mess) 
# Affichage de la fenêtre   
app.mainloop()