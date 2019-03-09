'''
For each item being considered, find the maximum value for whole knapsack.
To do this, consider value of the whole knapsack with and without the current
item.

WITH current item -> max value @ capacity == (current capacity - item weight)
WITHOUT current item -> max value @ capacity == current capacity.

Let the knapsack value be denoted by V[i][c] where i is the item number, and
c is the available capacity in the knapsack.

Then for any value V[i][c] in the matrix V, V[i][c] should be the maximum
value of the knapsack WITH the current item:
    V[i-1][c - items[i].weight] + items[i].value

and of the knapsack WITHOUT the current item:
    V[i-1][c]
'''
import time
import random
from collections import namedtuple

loot_adjectives = ['red', 'green', 'blue', 'crystal', 'explosive', 'death',
                   'underworld', 'secret', 'gravity', 'electron', 'dark']
items_to_loot = ['clock', 'map', 'ammo', 'bomb', 'cash', 'sword', 'portal']

class ThiefsKnapsack:
    def __init__(self, num_items=3, capacity=5):
        items = []
        item = namedtuple('item', ('name', 'value', 'weight'))
        for _ in range(num_items):
            new_item = item(
                random.choice(loot_adjectives) + ' ' + random.choice(
                items_to_loot),
                random.randrange(5, 100, 5),
                random.randrange(1, 10),)
            items.append(new_item)

        self.items = items
        self.capacity = capacity

        # Create 2D matrix, V[i][j], of values.
        self.matrix = [[None] * (self.capacity + 1) for _ in self.items]

        self.optimize_booty()

    def optimize_booty(self):
        V = self.matrix
        def _optimize_booty(i, j):
            if i < 0:
                # Recursive base case.  No items to choose from.
                return 0

            if V[i][j] == None:
                # Calculate max value in knapsack for item i, given a max
                # capacity of j.

                # without_item_i = V[i-1][j]
                without_item_i = _optimize_booty(i-1, j)

                # with_item_i = V[i-1][j-items[i].weight]
                with_item_i = (0 if self.items[i].weight > j else(
                    self.items[i].value + _optimize_booty(i-1, j-self.items[
                    i].weight)))

                V[i][j] = max(with_item_i, without_item_i)
                print(f'i:{i} j:{j} \t {self.items[i].name}')
                self.print_matrix()
                print()

            return V[i][j]

        optimal_booty = _optimize_booty(len(self.items)-1, self.capacity)
        print(f'Optimal Booty: {optimal_booty}')
        return optimal_booty


    def print_matrix(self):
        top_row = ' ' * 15
        for j in range(self.capacity + 1):
            top_row += str(j).center(8)
        underline = '-' * len(top_row)
        matrix_text = top_row + '\n' + underline + '\n'
        for i, row in enumerate(self.matrix):
            row_text = str(self.items[i].name).ljust(15)
            for cell in row:
                cell_text = '|' + str(cell).center(6) + '|'
                row_text += cell_text
            matrix_text += row_text + '\n'

        print(matrix_text)
        time.sleep(0.75)


    def print_items(self):
        for n, v, w in self.items:
            print(n, '\t\t', '$'+str(v), '\t', str(w)+'g')

new_knapsack = ThiefsKnapsack()
