from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
from util import Queue, Stack
import json
import random

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
current = player.current_room.id
reverse_path = []
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room.id)
fast_path = []

traversal_graph = {}

for i in range(len(room_graph)):
    copy = room_graph[i][1].copy()
    if 'n' in copy:
        copy['n'] = 'x'
    if 's' in copy:
        copy['s'] = 'x'
    if 'e' in copy:
        copy['e'] = 'x'
    if 'w' in copy:
        copy['w'] = 'x'
    traversal_graph[i] = copy

go_back = {}
for i in range(len(room_graph)):
    copy = room_graph[i][1].copy()
    go_back[i] = {value: key for key, value in copy.items()}

stack = Stack()
stack.push(player.current_room.id)


def dft(current=player.current_room.id):
    string = json.dumps(traversal_graph[current])
    while 'x' in string:
        direction = []
        for i in traversal_graph[current]:
            if traversal_graph[current][i] == 'x':
                direction.append(i)

        command = random.choice(direction)

        if command == 'n':
            traversal_graph[current]['n'] = room_graph[current][1]['n']
            player.travel('n')
            traversal_path.append(command)
            current = player.current_room.id
            traversal_graph[current]['s'] == room_graph[current][1]['s']
            string = json.dumps(traversal_graph[current])
        elif command == 's':
            traversal_graph[current]['s'] = room_graph[current][1]['s']
            player.travel('s')
            traversal_path.append(command)
            current = player.current_room.id
            traversal_graph[current]['n'] == room_graph[current][1]['n']
            string = json.dumps(traversal_graph[current])
        elif command == 'e':
            traversal_graph[current]['e'] = room_graph[current][1]['e']
            player.travel('e')
            traversal_path.append(command)
            current = player.current_room.id
            traversal_graph[current]['w'] == room_graph[current][1]['w']
            string = json.dumps(traversal_graph[current])
        elif command == 'w':
            traversal_graph[current]['w'] = room_graph[current][1]['w']
            player.travel('w')
            traversal_path.append(command)
            current = player.current_room.id
            traversal_graph[current]['e'] == room_graph[current][1]['e']
            string = json.dumps(traversal_graph[current])
    return bfs(current)


def bfs(current=player.current_room.id):
    queue = Queue()
    queue.enqueue([current])
    visited = set()

    while queue.size() > 0:
        path = queue.dequeue()
        v = path[-1]
        string = json.dumps(traversal_graph[v])
        if v not in visited:
            if 'x' in string:
                for i in range(len(path) - 1):
                    reversal = go_back[path[i]][path[i+1]]
                    player.travel(reversal)
                    traversal_path.append(reversal)
                    current = player.current_room.id
                return dft(current)
            visited.add(v)
            for neighbor in room_graph[v][1]:
                path2 = path.copy()
                path2.append(room_graph[v][1][neighbor])
                queue.enqueue(path2)


dft(player.current_room.id)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
