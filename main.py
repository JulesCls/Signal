from user import User
from server import Server


if __name__ == "__main__":
    s1 = Server()
    
    alice = User("Alice")

    alice.send_message("salut","bob")