class Node():
    def __init__(self, key):
        self.key = key
        self.parent = None
        self.first_child = None
        self.next_sibling = None

    def __str__(self):
        return self.key

    def set_first_child(self, key):
        child = Node(key)
        child.parent = self
        self.first_child = child

        return child

    def set_siblings(self, *keys):
        self.set_first_child(keys[0])
        node = self.child()
        for i in keys[1:]:
            node.set_next_sibling(i)
            node = node.n_sibling()

    def set_next_sibling(self, key):
        sibling = Node(key)
        sibling.parent = self.parent
        self.next_sibling = sibling

    def child(self):
        return self.first_child

    def n_sibling(self, times=None):
        if times == None:
            return self.next_sibling
        else:
            node = self
            for i in range(times):
                node = node.n_sibling()
                if node == None:
                    return
            return node

    def pre_traverse(self):
        s = self.key
        if self.first_child != None:
            s = s + self.first_child.pre_traverse()
        if self.next_sibling != None:
            s = s + self.next_sibling.pre_traverse()
        return s

    def pre_traverse_noreq(self):
        s = ''
        q_top = []
        temp_node = self
        while len(q_top) or temp_node:
            s = s + temp_node.key
            if temp_node.first_child:
                if temp_node.next_sibling:
                    q_top.append(temp_node.n_sibling())
                temp_node = temp_node.child()
                continue
            if temp_node.next_sibling:
                temp_node = temp_node.n_sibling()
            elif len(q_top):
                temp_node = q_top.pop()
            else:
                temp_node = None

        return s

    def post_traverse(self):
        s = self.key
        if self.first_child != None:
            s = self.first_child.post_traverse() + s
        if self.next_sibling != None:
            s = s + self.next_sibling.post_traverse()
        return s

    def level_traverse(self):
        s = ''
        q = [
            self,
        ]
        while len(q) != 0:
            node = q.pop(0)
            s = s + node.key
            if node.first_child:
                temp_node = node.child()
                q.append(temp_node)
                while temp_node.n_sibling():
                    q.append(temp_node.n_sibling())
                    temp_node = temp_node.n_sibling()
        return s
