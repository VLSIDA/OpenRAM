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


    def iterate_point(self, point, check_done=False):
        """ Iterate over shapes in the tree that overlap the given point. """

        px, py = point.x, point.y
        # Return this shape if it's a leaf
        if self.is_leaf:
            ll, ur = self.bbox.rect
            if check_done or (ll.x <= px and px <= ur.x and ll.y <= py and py <= ur.y):
                yield self.bbox.shape
        else:
            # Check the left child
            if self.left:
                ll, ur = self.left.bbox.rect
                if ll.x <= px and px <= ur.x and ll.y <= py and py <= ur.y:
                    yield from self.left.iterate_point(point, True)
            # Check the right child
            if self.right:
                ll, ur = self.right.bbox.rect
                if ll.x <= px and px <= ur.x and ll.y <= py and py <= ur.y:
                    yield from self.right.iterate_point(point, True)


    def iterate_shape(self, shape, check_done=False):
        """ Iterate over shapes in the tree that overlap the given shape. """

        sll, sur = shape.rect
        # Return this shape if it's a leaf
        if self.is_leaf:
            ll, ur = self.bbox.rect
            if check_done or (ll.x <= sur.x and sll.x <= ur.x and ll.y <= sur.y and sll.y <= ur.y):
                yield self.bbox.shape
        else:
            # Check the left child
            if self.left:
                ll, ur = self.left.bbox.rect
                if ll.x <= sur.x and sll.x <= ur.x and ll.y <= sur.y and sll.y <= ur.y:
                    yield from self.left.iterate_shape(shape, True)
            # Check the right child
            if self.right:
                ll, ur = self.right.bbox.rect
                if ll.x <= sur.x and sll.x <= ur.x and ll.y <= sur.y and sll.y <= ur.y:
                    yield from self.right.iterate_shape(shape, True)


    def get_costs(self, bbox):
        """ Return the costs of bbox nodes after merging the given bbox. """

        # Find the new areas for all possible cases
        self_merge = bbox.merge(self.bbox)
        left_merge = bbox.merge(self.left.bbox)
        right_merge = bbox.merge(self.right.bbox)

        # Add the change in areas as cost
        self_cost = self_merge.area()
        left_cost = self_merge.area() - self.bbox.area()
        left_cost += left_merge.area() - self.left.bbox.area()
        right_cost = self_merge.area() - self.bbox.area()
        right_cost += right_merge.area() - self.right.bbox.area()

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

        if self.is_leaf:
            # Put the current bbox to the left child
            self.left = bbox_node(self.bbox)
            # Put the new bbox to the right child
            self.right = bbox_node(bbox)
        else:
            # Calculate the costs of adding the new bbox
            self_cost, left_cost, right_cost = self.get_costs(bbox)
            if self_cost < left_cost and self_cost < right_cost: # Add here
                self.left = bbox_node(self.bbox, left=self.left, right=self.right)
                self.right = bbox_node(bbox)
            elif left_cost < right_cost: # Add to the left
                self.left.insert(bbox)
            else: # Add to the right
                self.right.insert(bbox)
        # Update the current bbox
        self.bbox = self.left.bbox.merge(self.right.bbox)
        self.is_leaf = False
