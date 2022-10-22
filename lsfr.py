import secrets
import utils
import queue as q

def xorshift():
    input = utils.generateRandomSplitInt(128,4)
    return 

if __name__ == "__main__":
    q = q.Queue(4)
    for x in range(4):
        q.put(x)
    print("Members of the queue:")
    for n in list(q.queue):
        print(n, end=" ")
    print("\nSize of the queue:")
    print(q.qsize())
    q.put(4)
    for n in list(q.queue):
        print(n, end=" ")
    print("\nSize of the queue:")
    print(q.qsize())

    