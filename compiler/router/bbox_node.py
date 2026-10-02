# See LICENSE for licensing information.
#
# Copyright (c) 2016-2024 Regents of the University of California, Santa Cruz
# All rights reserved.
#

class bbox_node:
    """
    This class represents a node in the bbox tree structure. Bbox trees are
    binary trees we use to partition the shapes in the routing region so that
    we can detect overlaps faster in a binary search-like manner.
    """

    def __init__(self, bbox, left=None, right=None):

        self.bbox = bbox
        self.is_leaf = not left and not right
        self.left = left
        self.right = right


    def iterate_point(self, point):
        """ Iterate over shapes in the tree that overlap the given point. """

        px, py = point.x, point.y
        ll, ur = self.bbox.rect
        if not (ll.x <= px <= ur.x and ll.y <= py <= ur.y):
            return
        # Depth first, left before right, with a stack rather than recursion
        # (the tree can get deeper than Python's recursion limit). Only nodes
        # whose bbox contains the point are pushed, so a leaf on the stack is a
        # match.
        stack = [self]
        while stack:
            node = stack.pop()
            if node.is_leaf:
                yield node.bbox.shape
                continue
            # Push the right child first so that the left one comes first
            for child in (node.right, node.left):
                if child:
                    ll, ur = child.bbox.rect
                    if ll.x <= px <= ur.x and ll.y <= py <= ur.y:
                        stack.append(child)


    def iterate_shape(self, shape):
        """ Iterate over shapes in the tree that overlap the given shape. """

        sll, sur = shape.rect
        ll, ur = self.bbox.rect
        if not (ll.x <= sur.x and sll.x <= ur.x and ll.y <= sur.y and sll.y <= ur.y):
            return
        # Depth first, left before right, with a stack rather than recursion
        # (the tree can get deeper than Python's recursion limit). Only nodes
        # whose bbox overlaps the shape are pushed, so a leaf on the stack is a
        # match.
        stack = [self]
        while stack:
            node = stack.pop()
            if node.is_leaf:
                yield node.bbox.shape
                continue
            # Push the right child first so that the left one comes first
            for child in (node.right, node.left):
                if child:
                    ll, ur = child.bbox.rect
                    if ll.x <= sur.x and sll.x <= ur.x and ll.y <= sur.y and sll.y <= ur.y:
                        stack.append(child)


    def get_costs(self, bbox):
        """ Return the costs of bbox nodes after merging the given bbox. """

        # Find the new areas for all possible cases
        self_merge = bbox.merge(self.bbox)
        left_merge = bbox.merge(self.left.bbox)
        right_merge = bbox.merge(self.right.bbox)

        # Add the change in areas as cost
        self_cost = self_merge.area()
        growth = self_cost - self.bbox.area()
        left_cost = growth + (left_merge.area() - self.left.bbox.area())
        right_cost = growth + (right_merge.area() - self.right.bbox.area())

        # Add the overlaps in areas as cost
        self_overlap = self.bbox.overlap(bbox)
        left_overlap = left_merge.overlap(self.right.bbox)
        right_overlap = right_merge.overlap(self.left.bbox)
        if self_overlap:
            self_cost += self_overlap.area()
        if left_overlap:
            left_cost += left_overlap.area()
        if right_overlap:
            right_cost += right_overlap.area()

        return self_cost, left_cost, right_cost


    def insert(self, bbox):
        """ Insert a bbox to the bbox tree. """

        # Go down to the node where the bbox is added. This is a loop rather
        # than recursion because the tree can get deeper than Python's
        # recursion limit in large designs.
        path = []
        node = self
        while True:
            path.append(node)
            if node.is_leaf:
                # Put the current bbox to the left child
                node.left = bbox_node(node.bbox)
                # Put the new bbox to the right child
                node.right = bbox_node(bbox)
                break
            # Calculate the costs of adding the new bbox
            self_cost, left_cost, right_cost = node.get_costs(bbox)
            if self_cost < left_cost and self_cost < right_cost: # Add here
                node.left = bbox_node(node.bbox, left=node.left, right=node.right)
                node.right = bbox_node(bbox)
                break
            elif left_cost < right_cost: # Add to the left
                node = node.left
            else: # Add to the right
                node = node.right
        # Update the bboxes on the way back up
        for node in reversed(path):
            node.bbox = node.left.bbox.merge(node.right.bbox)
            node.is_leaf = False
