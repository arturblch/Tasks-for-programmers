# Задача: Обратить порядок расположенияэлементов в односвязном списке за O(n) времени и О(1) памяти.
class Node:
    def __init__(self, data=0):
        self.data = data
        self._next = None

    @staticmethod
    def reverse(head):
        prev = None
        cur = head
        next_ = None
        while (cur != None):
            next_ = cur._next
            cur._next = prev
            prev = cur
            cur = next_
        return prev

    def push(self, new_data):
        new_node = Node()
        new_node.data = new_data
        new_node._next = self
        return new_node

    def print(self):
        temp = self
        while (temp != None):
            print(temp.data, end=' ')
            temp = temp._next


head = Node(5)
head = head.push(20)
head = head.push(4)
head = head.push(15)
head = head.push(82)

head.print()
head = Node.reverse(head)
print('')
head.print()
