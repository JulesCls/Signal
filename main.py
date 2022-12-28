from user import User
from server import Server

def show_channel_possibilites():
    print("="*50)
    print("Que souhaitez-vous faire ? ")
    print("  1  -- Envoyer un message")
    print("  2  -- Envoyer un fichier")
    print("  3  -- Lire vos messages")
    print("quit -- quitter")

def execute_input(input_str:str,user:User,target:str):
    if input_str == "1":
        message = input("Saisir le message :")
        try:
            user.send_message(message,target)
        except Exception as e:
            print("*"*20 + "Erreur" + "*"*20)
            print(f"Impossible d'envoyer le message : {e}")
            print("*"*50)
    elif input_str == "2":
        filepath = input("Saisir le chemin complet du fichier :")
        try:
            user.send_message(filepath,target,is_file=True)
        except Exception as e:
            print("*"*20 + "Erreur" + "*"*20)
            print(f"Impossible d'envoyer le message : {e}")
    elif input_str == "3":
        user.print_target_conversation(target)


def channel_connection(user:User,target_name:str):
    user.connect_to_target(target_name)
    user_input = ""
    while user_input != "quit":
        user.print_target_conversation(target_name)
        show_channel_possibilites()
        user_input = input("Choix :")
        if user_input != "quit":
            execute_input(user_input,user,target_name)
    



import os

if __name__ == "__main__":
    # server = Server()
    
    # alice = User("alice")
    # bob = User("bob")
    # alice.connect_to_target('bob')
    # bob.connect_to_target('alice')
    # bob.print_target_conversation("alice")
    # bob.send_message("comment vas-tu alice ?","alice")
    # bob.print_target_conversation("alice")


    
    # alice.connect_to_server()
    # alice.send_message("salut comment vas-tu mon amis","bob")
    # alice.send_message("c'est alice","bob")
    # bob = User("bob")
    # bob.connect_to_server()
    # bob.get_pending_messages()
    # bob.send_message("hey alice comment vas-tu ?","alice")
    # bob.send_message("je suis allé au parc hier","alice")
    # alice.get_pending_messages()
    # alice._sks["bob"] = None
    # alice.send_message("je suis allé au parc hier","bob")
    # bob.get_pending_messages()
    # bob.send_message("je suis allé au parc hier moi aussi","alice")
    # alice.get_pending_messages()

    # # alice.send_message("salut","bob")

    user_input = input("Entrez votre nom d'utilisateur:")
    user = User(user_input)
    print(f"Bonjour {user.get_name()}:")
    print("Il est possible de quitter l'application en utilisant la commande 'quit'")
    while user_input != "quit":
        user_input = input("A quel utilisateur souhaitez vous envoyer un message : ")
        channel_connection(user,user_input)
        




    