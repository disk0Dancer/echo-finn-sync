import threading
import time

from pika_client import *

class FinnNode:
    def __init__(self, node_id, neighbors_in: list, neighbors_out: list):
        """
        Инициализация узла.
        :param node_id: Уникальный идентификатор узла.
        :param neighbors_in: Список входящих соседей.
        :param neighbors_out: Список исходящих соседей.
        """
        self.node_id = node_id
        self.neighbors_in = neighbors_in
        self.neighbors_out = neighbors_out
        self.inc = {self.node_id}
        self.ninc = set()
        self.received_messages = set()
        self.active = False
        self.completed = False

    def start(self):
        threading.Thread(target=self.listen).start()

    def listen(self):
        queue_name = f"node_{self.node_id}"
        consume_messages(queue_name, self.on_receive_message)

    def on_receive_message(self, message):
        sender = message["sender"]
        inc_received = set(message["inc"])
        ninc_received = set(message["ninc"])

        self.inc.update(inc_received)
        self.ninc.update(ninc_received)
        self.received_messages.add(sender)

        print(f"Node {self.node_id} received from {sender}: INC={inc_received}, NINC={ninc_received}")
        print(f"Node {self.node_id} updated INC={self.inc}, NINC={self.ninc}")

        if len(self.received_messages) == len(self.neighbors_in):
            self.ninc.add(self.node_id)

            if self.inc == self.ninc:
                print(f"Node {self.node_id} завершил алгоритм. INC={self.inc}, NINC={self.ninc}")
                self.completed = True
                return

            for neighbor in self.neighbors_out:
                send_message(f"node_{neighbor}", {"sender": self.node_id, "inc": list(self.inc), "ninc": list(self.ninc)})

    def initiate(self):
        """
        Инициализация алгоритма.
        """
        self.active = True
        print(f"Node {self.node_id} initiating algorithm...")
        for neighbor in self.neighbors_out:
            send_message(f"node_{neighbor}",
                         {"sender": self.node_id, "inc": list(self.inc), "ninc": list(self.ninc)})


if __name__ == "__main__":
    # nodes = {
    #     1: FinnNode(1, [2], [2, 3, 4]),
    #     2: FinnNode(2, [1, 3], [1]),
    #     3: FinnNode(3, [1, 4], [2]),
    #     4: FinnNode(4, [1], [3]),
    # }
    # 0 0 0 1
    # 1 0 0 0
    # 1 1 0 0
    # 1 0 1 0

    nodes = {
        1: FinnNode(1, [], [2, 3]),
        2: FinnNode(2, [1], [4]),
        3: FinnNode(3, [1], []),
        4: FinnNode(4, [2], [])
    }
    
    # 1 1 1 0
    # 0 1 0 1
    # 0 0 1 0
    # 0 0 0 1
    
    for node in nodes.values():
        node.start()
        time.sleep(0.1)
    
    time.sleep(1)
    
    nodes[1].initiate()
