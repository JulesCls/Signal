from user import User
from server import Server

def show_possibilites():
    print("-"*50)
    print("Que souhaitez-vous faire ? ")
    print("  1  -- Envoyer un message à un utilisateur")
    print("  2  -- Lire vos messages")
    print("quit -- quitter")

def execute_input(input_str:str,user:User):
    if input_str == "1":
        target_user = input("A quel utilisateur souhaitez-vous envoyer un message :")
        message = input("Saisir le message :")
        try:
            user.send_message(message,target_user)
        except Exception as e:
            print("*"*20 + "Erreur" + "*"*20)
            print(f"Impossible d'envoyer le message : {e}")
    elif input_str == "2":
        user.get_pending_messages()



if __name__ == "__main__":
    # server = Server()
    
    # alice = User("alice")
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

    # alice.send_message("salut","bob")

    user_input = input("Entrez votre nom d'utilisateur:")
    user = User(user_input)
    user.connect_to_server()
    print(f"Bonjour {user.get_name()}:")
    while user_input != "quit":
        show_possibilites()
        user_input = input("choix :")
        execute_input(user_input,user)
        




    