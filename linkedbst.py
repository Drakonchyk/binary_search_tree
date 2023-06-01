"""
File: linkedbst.py
Author: Ken Lambert
"""
import time
import random
from math import log2
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack



class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            strng = ""
            if node is not None:
                strng += recurse(node.right, level + 1)
                strng += "| " * level
                strng += str(node.data) + "\n"
                strng += recurse(node.left, level + 1)
            return strng

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = []

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""
        current = self._root

        while current is not None:
            if item == current.data:
                return current.data
            if item < current.data:
                current = current.left
            else:
                current = current.right

        return None

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""
        new_node = BSTNode(item)

        if self.isEmpty():
            self._root = new_node
            self._size += 1
            return

        current = self._root
        parent = None

        while current is not None:
            parent = current
            if item < current.data:
                current = current.left
            else:
                current = current.right

        if item < parent.data:
            parent.left = new_node
        else:
            parent.right = new_node

        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_left_subtree(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            curr_node = top.left
            while not curr_node.right is None:
                parent = curr_node
                curr_node = curr_node.right
            top.data = curr_node.data
            if parent == top:
                top.left = curr_node.left
            else:
                parent.right = curr_node.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        curr_node = self._root
        while not curr_node is None:
            if curr_node.data == item:
                item_removed = curr_node.data
                break
            parent = curr_node
            if curr_node.data > item:
                direction = 'L'
                curr_node = curr_node.left
            else:
                direction = 'R'
                curr_node = curr_node.right

        # Return None if the item is absent
        if item_removed is None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not curr_node.left is None \
                and not curr_node.right is None:
            lift_left_subtree(curr_node)
        else:

            # Case 2: The node has no left child
            if curr_node.left is None:
                new_child = curr_node.right

                # Case 3: The node has no right child
            else:
                new_child = curr_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with new_item and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            if probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''
        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return -1
            left_h = height1(top.left)
            right_h = height1(top.right)
            return 1 + max(left_h, right_h)
        if self._root is None:
            return 0
        return height1(self._root)


    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        def node_num(node):
            if node is None:
                return 0
            return 1 + node_num(node.left) + node_num(node.right)
        sum_nodes = node_num(self._root)
        return self.height() < (2*log2(sum_nodes + 1) - 1)


    def range_find(self, low, high):
        """
        Returns a list of the items in the tree, where low <= item <= high.
        :param low: The lower bound value.
        :param high: The upper bound value.
        :return: A list of items within the specified range.
        """
        result = []
        self._range_find_helper(self._root, low, high, result)
        return result

    def _range_find_helper(self, node, low, high, result):
        """
        Helper function for the rangeFind method.
        :param node: The current node being examined.
        :param low: The lower bound value.
        :param high: The upper bound value.
        :param result: The list to store the items within the range.
        """
        if node is None:
            return

        if node.data >= low:
            self._range_find_helper(node.left, low, high, result)

        if low <= node.data <= high:
            result.append(node.data)

        if node.data <= high:
            self._range_find_helper(node.right, low, high, result)

    def rebalance(self):
        """
        Rebalances the tree to improve its efficiency.
        """
        tree_list = list(self.inorder())
        self.clear()
        self._build_balanced_tree(tree_list)

    def _build_balanced_tree(self, tree_list):
        """
        Helper function to build a balanced tree from a sorted list of nodes.
        :param nodes: The sorted list of nodes.
        :param low: The lower index of the sublist.
        :param high: The upper index of the sublist.
        :return: The root node of the balanced tree.
        """
        if tree_list:
            mid = len(tree_list) // 2
            self.add(tree_list[mid])
            self._build_balanced_tree(tree_list[:mid])
            self._build_balanced_tree(tree_list[1+mid:])


    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        successor = None
        node = self._root

        while node is not None:
            if item < node.data:
                successor = node.data
                node = node.left
            else:
                node = node.right

        return successor

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        predecessor = None
        node = self._root

        while node is not None:
            if item > node.data:
                predecessor = node.data
                node = node.right
            else:
                node = node.left

        return predecessor

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        with open(path, 'r', encoding='utf-8') as file:
            dictionary = [word.strip() for word in file.readlines()]


        start_time = time.time()
        for _ in range(10000):
            word = dictionary[random.randint(0, len(dictionary)-1)]
            _ = word in dictionary
        list_search_time = time.time() - start_time

        # Task 2: Search in ordered dictionary using binary search tree
        bst_ordered = LinkedBST(dictionary)
        start_time = time.time()
        for _ in range(100):
            word = dictionary[random.randint(0, len(dictionary)-1)]
            _ = bst_ordered.find(word)
        bst_ordered_search_time = time.time() - start_time

        # Task 3: Search in unordered dictionary using binary search tree
        random.shuffle(dictionary)
        bst_unordered = LinkedBST(dictionary)
        start_time = time.time()
        for _ in range(10000):
            word = dictionary[random.randint(0, len(dictionary)-1)]
            _ = bst_unordered.find(word)
        bst_unordered_search_time = time.time() - start_time

        # Task 4: Search in balanced binary search tree
        bst_unordered.rebalance()
        start_time = time.time()
        for _ in range(10000):
            word = dictionary[random.randint(0, len(dictionary)-1)]
            _ = bst_unordered.find(word)
        bst_balanced_search_time = time.time() - start_time

        # Display the results
        print("Time to search 10000 random words in an ordered dictionary (list):",
              list_search_time)
        print("Time to search 10000 random words in an ordered dictionary (BST):",
              bst_ordered_search_time)
        print("Time to search 10000 random words in an unordered dictionary (BST):",
              bst_unordered_search_time)
        print("Time to search 10000 random words in a balanced dictionary (BST):",
              bst_balanced_search_time)
