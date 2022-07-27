import numpy as np
import random as rand

ALIVE = True
DEAD = False

class Grid:
    def __init__(self, rows, cols):
        if rows < 0 or cols < 0:
            raise Exception()
        self.rows = rows
        self.cols = cols
        self.state = np.zeros((self.rows, self.cols), dtype=bool)
    
    def clear_state(self):
        self.state = np.zeros((self.rows, self.cols), dtype=bool)

    def in_bounds(self, i, j):
        return 0 <= i < self.rows and 0 <= j < self.cols

    def get_cell(self,i,j):
        if self.in_bounds(i,j):
            return self.state[i][j]

    def set_cell(self,i,j,value):
        if self.in_bounds(i,j):
            self.state[i][j] = value

    def randomize(self,threshold):
        self.clear_state()
        for i in range(self.rows):
            for j in range(self.cols):
                if (rand.random() < threshold):
                    self.state[i][j] = ALIVE

    def surrounding_alive_count(self,i,j):
        if not self.in_bounds(i,j): return
        count = 0
        for n_i in range(i-1,i+2):
            for n_j in range(j-1,j+2):
                if (n_i == i and n_j == j): continue;
                if self.in_bounds(n_i,n_j) and self.state[n_i][n_j] == ALIVE: 
                    count+=1
        return count

    def evolve(self):
        new_state = np.copy(self.state)
        for i in range(self.rows):
            for j in range(self.cols):
                alive_count = self.surrounding_alive_count(i,j)
                curr_state = self.state[i][j]
                # live condition
                if (alive_count == 3) or (alive_count == 2 and curr_state == ALIVE):
                    new_state[i][j] = ALIVE
                else:
                    new_state[i][j] = DEAD
        self.state = new_state
