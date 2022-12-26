from user import User
from server import Server


if __name__ == "__main__":
    server = Server()
    
    alice = User("Alice")
    bob = User("Bob")
    
    alice.connect_to_conversation(bob.get_name())
    bob.connect_to_conversation(alice.get_name())

    # alice.send_message("salut","bob")