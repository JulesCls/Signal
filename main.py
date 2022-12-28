from user import User
from server import Server


if __name__ == "__main__":
    server = Server()
    
    alice = User("alice")
    bob = User("bob")
    alice.connect_to_server()
    bob.connect_to_server()
    alice.send_message("salut comment vas-tu mon amis","aaaa")
    alice.send_message("c'est alice","bob")
    bob.get_pending_messages()
    bob.send_message("hey alice comment vas-tu ?","alice")
    bob.send_message("je suis allé au parc hier","alice")
    alice.get_pending_messages()
    alice._sk["message_key"] = None
    alice.send_message("je suis allé au parc hier","bob")
    bob.get_pending_messages()
    bob.send_message("je suis allé au parc hier moi aussi","aaa")
    alice.get_pending_messages()


    print(alice._sk)
    print(bob._sk)
    # alice.send_message("salut","bob")