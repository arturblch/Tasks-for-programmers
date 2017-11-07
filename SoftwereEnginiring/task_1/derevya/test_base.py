import pytest
from tree_example import Node


def setup():
    global tree
    tree = bild_tree()


def bild_tree():
    root = Node('E')
    root.set_siblings('B', 'F', 'M')

    root.child().set_siblings('A', 'C')
    root.child().child().n_sibling().set_first_child('D')

    root.child().n_sibling().set_siblings('G', 'H', 'I', 'L')
    root.child().n_sibling().child().n_sibling(2).set_siblings('J', 'K')

    root.child().n_sibling(2).set_first_child('N')

    return root


def test_preorder_traversal():
    assert tree.pre_traverse() == 'EBACDFGHIJKLMN'
    assert tree.pre_traverse_noreq() == 'EBACDFGHIJKLMN'

def test_postorder_traversal():
    assert tree.post_traverse() == 'ADCBGHJKILFNME'

def test_inorder_traversal():
    assert tree.level_traverse() == 'EBFMACGHILNDJK'


# E{
#     B{
#         A{}
#         C{D}
#     }
#     F{
#         G{}
#         H{}
#         I{JK}
#         L{}
#     }
#     M{N}
# }