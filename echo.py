import threading
import time

from pika_client import *


class EchoNode:
    def __init__(self, node_id, neighbors: list):
        self.node_id = node_id
        self.neighbors = neighbors
        self.received_messages = []
        self.parent = None
        self.first = False

    def start(self):
        threading.Thread(target=self.listen).start()

    def listen(self):
        queue_name = f"node_{self.node_id}"
        consume_messages(queue_name, self.on_receive_message)

    def on_receive_message(self, message):
        sender = message["sender"]
        self.received_messages.append(sender)

        if self.parent is None:
            self.parent = sender

        if len(self.received_messages) == len(self.neighbors):
            print(f"-> Node {self.node_id} finished")
            if not self.first:
                send_message(f"node_{self.parent}", {"sender": self.node_id})
            return
        
        else:
            for neighbor in self.neighbors:
                if neighbor != sender:
                    send_message(f"node_{neighbor}", {"sender": self.node_id})
                    time.sleep(1)
            
        if self.first:
            print(f"-> Node {self.node_id} msgs : {self.received_messages}")

    def initiate(self):
        self.parent = None
        self.first = True
        print(f"Node {self.node_id} initiating algorithm...")
        for neighbor in self.neighbors:
            send_message(f"node_{neighbor}", {"sender": self.node_id})
            time.sleep(1)


if __name__ == "__main__":
    nodes = {
        1: EchoNode(1, [2, 3]),
        2: EchoNode(2, [1]),
        3: EchoNode(3, [1]),
        4: EchoNode(4, [3]),
    }
    
    # |--> 3 -> 4
    # 1 -> 2

    
    # 1 1 1 0
    # 1 1 0 1
    # 1 0 1 0
    # 0 1 0 1
    
    for node in nodes.values():
        node.start()
        time.sleep(0.1)
    
    time.sleep(1)
    nodes[1].initiate()
