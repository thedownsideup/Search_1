#!/usr/bin/env python
# coding: utf-8

# ## Search: A*, BFS, IDS
# 
# ### 2 Pacmans looking for food
# 
# ### Mahsa Eskandari Ghadi
# 
# 
# *In this report by "we" I mean me and the person reading this cuz we are on the same boat :))*

# ### Part A
# 
# Needed modules are imported. Test files for testcases are read line by line (forms the board) and character by character; Incase there's any food it's coordinates are linked to that special character in our food dictionary right away.

# In[23]:


import sys, time
from collections import deque
from math import sqrt

board = []
foods_dict = {'1':[], '2':[], '3': []}
with open('test5', 'r') as f:
    for i, line in enumerate(f):
        board.append(list(line))
        for j, char in enumerate(line):
            if char in ['1', '2', '3']:
                foods_dict[char].append([i, j])


# To see the board at anytime:

# In[24]:


def print_board(board):
    for line in board:
        for char in line:
            print(char, end = '')


# This functions is written for the A* algorithm. Targeted foods are ['1','3'] or ['2','3'] depending on which pacman we're focusing on.
# 
# To estimate the cost of reaching the goal state we do as we learned in class : [f(n)=g(n)+h(n)] where h is the length of reaching the goal with a straight line(Euclidean distance) and g is the depth(because each step's cost is always 1)
# 
# First it finds the distance to the first target as a starting point then it calculates other distances if there's one closer, then the distance is replaced with the shorter distance. 

# In[25]:


def near_food_distance(queue_item, targeted_foods):
    distance = sqrt((targeted_foods[0][0] - queue_item[0])**2 + (targeted_foods[0][1] - queue_item[1]) ** 2)
    targeted_foods.pop(0)
    for targeted_food in targeted_foods:
        d = sqrt((targeted_food[0] - queue_item[0])**2 + (targeted_food[1] - queue_item[1]) ** 2)
        distance = d if distance > d else distance
    return queue_item[2] + distance


# ### Part B
# 
# The search function is where different search methods are seperated.
# 
# - search_type : BFS, IDS, A*
# - board : the map we've read previously
# - source : the staring point of pacman (P or Q).
# - targeted_list : same as before
# - avoid_list : the poison for each pacman (again seperately; for P 2 and for Q 1) plus walls('%').
# 
# #### Algorithms
# 
# 1. BFS : 
#     Eachtime we check the four surrounding blocks; if it's not a wall or poison or visited it's appended to the path. If it's a target, it's deleted(eaten) then the path is returned.
#  
# 2. IDS : 
#     Again eachtime the four surrounding blocks are checked. This time if we haven't passed the depth limit we append the empty space or target to the beginning of the queue and path. Then we reset visited, start queue and path from the source again and increase depth limit to search one layer further in the next loop.
#     
# 3. A* : 
#     We do this for every food in the target list:
#     We sort queue and paths. The first item of the queue list and the last item of the paths are our starting point because we're appending to the end and checking them eachtime to see if it's the goal so the right most child is the one that it's children contain the goal.

# In[26]:


def search(search_type, board, source, target_list, avoid_list):
    queue = deque([source])
    paths = deque([[source]])
    visited = [[' ' for char in line] for line in board]

    depth_limit = 0
    states = 0

    while queue:


        if search_type == "A*":
            targeted_foods = []
            for target in target_list:
                targeted_foods += foods_dict[target]

            queue = deque(sorted(queue, key = lambda queue_item: near_food_distance(queue_item, targeted_foods.copy())))
            paths = deque(sorted(paths, key = lambda paths_item: near_food_distance(paths_item[-1], targeted_foods.copy())))

        current = queue.popleft()
        path = paths.popleft()

        states += 1

        if board[current[0]][current[1]] in target_list:
            board[current[0]][current[1]] = ' '
            return states, path
        
        visited[current[0]][current[1]] = 'v'
        
        near_list = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for near_cell in near_list:

            near = [current[0] + near_cell[0], current[1] + near_cell[1], current[2] + 1]

            if board[near[0]][near[1]] not in avoid_list and visited[near[0]][near[1]] != 'v':
                if search_type == "BFS" or search_type == "A*":
                    queue.append(near)
                    new_path = path.copy()
                    new_path.append(near)
                    paths.append(new_path)
                elif search_type == "IDS" and current[2] < depth_limit:
                    queue.appendleft(near)
                    new_path = path.copy()
                    new_path.append(near)
                    paths.appendleft(new_path)

        if not queue and search_type == 'IDS':
            queue = deque([source])
            paths = deque([[source]])
            visited = [[' ' for char in line] for line in board]
            depth_limit += 1


# This function find the position of the pacmans P and Q.

# In[27]:


def find_pacmans(board):
    p, q = (-1, -1), (-1, -1)
    for i, line in enumerate(board):
        for j, char in enumerate(line):
            if char == 'P':
                p = (i, j, 0)
            elif char == 'Q':
                q = (i, j, 0)
                
    return p, q


# This function checks if there's any food left on the map.

# In[28]:


def food_left(board, food_list):
    for line in board:
        for food in food_list:
            if line.count(food):
                return True
    return False


# This function basically runs the game(Ready), calls find pacmans(Set) , calls the search fuction with a specific search method (Go!), but the nokte is! that it calls p and q by turn. if there's no food left (YOU WIN! cuz you can't lose in this game)

# In[29]:


def play_game(board):

    p, q = find_pacmans(board)
    path_p, path_q = [], []

    i = 0
    sum_states = 0
    while 1:
        if i % 2 == 0 and food_left(board, ['1', '3']):
            states, path = search("BFS", board, [p[0], p[1], p[2]], ['1', '3'], ['%', '2', 'Q'])
            sum_states += states
            path_p += path
            p = path_p.pop()
        elif i % 2 == 1 and food_left(board, ['2', '3']):
            states, path = search("BFS", board, [q[0], q[1], q[2]], ['2', '3'], ['%', '1', 'P'])
            sum_states += states
            path_q += path
            q = path_q.pop()
        
        if not food_left(board, ['1', '2', '3']):
            break

        i += 1
    
    path_p.append(p)
    path_q.append(q)
    return sum_states, path_p, path_q


# In[30]:


t1 = time.time()
sum_states, path_p, path_q = play_game(board)
t2 = time.time()
print(t2 - t1)
print(path_p)
print(len(path_p))
print()
print(path_q)
print(len(path_q))
print(sum_states)


# ![table.png](attachment:table.png)

# As we can see from the results it's safe to say even tho BFS and IDS are faster in some cases A* is faster in bigger test cases and also it needs to travel much less(less visited states) to get to the goal. BFS is both faster and smarter in choosing paths than IDS. 

# Another thing to point out is that with the algorithm we've implemented we don't visit the same state twice because we check to see if it has or hasn't been visited before. That's why the number of "states visited" and "discrete states visited" are the same.
