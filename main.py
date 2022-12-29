
from user import User
from multiprocessing import Process

def show_channel_possibilites(user:User,target_name:str):
    print("="*50)
    print(f"{user.get_name()} que souhaitez-vous faire ? ")
    print(f"  1  -- Envoyer un message à {target_name}")
    print(f"  2  -- Envoyer un fichier à {target_name}")
    print("quit -- quitter")
    print("="*50)
    print("\n"*1)

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


def channel_connection(user:User,target_name:str):
    user.connect_to_target(target_name)
    user_input = ""
    while user_input != "quit":
        p = Process(target=user.print_target_conversation, args=(target_name,))
        p.daemon = True
        p = p.start()
        show_channel_possibilites(user,target_name)
        user_input = input()
        if user_input != "quit":
            execute_input(user_input,user,target_name)
    



import os

if __name__ == "__main__":
    user_input = input("Entrez votre nom d'utilisateur: ")
    user = User(user_input)
    print(f"Bonjour {user.get_name()} ! ")
    print("Il est possible de quitter l'application en utilisant la commande 'quit'")
    while user_input != "quit":
        user_input = input("A quel utilisateur souhaitez vous envoyer un message : ")
        channel_connection(user,user_input)
        




    