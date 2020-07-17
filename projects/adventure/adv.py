from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop()
        else:
            return None
    def size(self):
        return len(self.queue)

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# We need a dictionary to keep track of the rooms
visited = {} 

# we need a dictionary to reference each of the directions' opposite direction                                                    
retraced_steps = {                                              
    'n': 's',
    's': 'n',
    'e': 'w',
    'w': 'e'
}

# the starting room is the id of the room the player is currently in
starting_room = player.current_room.id                          

# instantiate a queue and insert the starting room
q = Queue()
q.enqueue(starting_room)

# instantiate a current path array, so we can have an array similiar to traversal_path, but manipulate it 
# without significant consequence, i.e., thake things off of it
temp_path = []

# set a while loop that runs as long as there are still rooms left to explore
while len(visited) < len(room_graph):
    # make cur_room pointer at the last room in the queue
    cur_room = q.dequeue()
    # get array consisting of directions that are possible for the room the player is currently in. 
    # i.e. exits = ['n', 'e']
    exits = player.current_room.get_exits()
    # make an array to keep track of where the player hasn't been yet. right now it's nothing
    exits_with_qs = []

    # check if the cur_room is not in the dictionary of rooms I made
    if cur_room not in visited:
        # if it's not, add cur_room as a key, and a blank dictionary for its value. 
        # i.e. visited = {'cur_room': {}}
        visited[cur_room] = {}
        # for each exit the cur_room has, 
        # i.e. exits = ['n', 'e']
        for exit in exits:
            # ...go into room dictionary, go further into the dictionary-as-value, and have direction equal ?
            # ex. visited = {cur_room: {'n': '?', 'e':'?'}}
            visited[cur_room][exit] = '?'

    # using dictionary deconstruction, go into the dictionary within the dictionary
    for direction, association in visited[cur_room].items():
        # check if it's associated with a room that hasn't been explored yet, aka has a ?. at first it will be all of them
        if association == '?':
            # if that's the case, then append the direction to the exits_with_qs list
            # i.e. exits_with_qs = ['n', 'e']
            exits_with_qs.append(direction)
    
    # check if there are known connections to the room the player is currently in that haven't been identified. if yes...
    if len(exits_with_qs) > 0:
        # set up random_exit pointer to find a random, undexplored direction in the array. 
        # i.e. random_exit = 'n'
        random_exit = random.choice(exits_with_qs)
        # using the retraced_steps reference dictionary, set up pointer at the reverse. 
        # i.e. reverse = 's'
        reverse = retraced_steps[random_exit]
        # have the player travel in the unexplored direction i.e. 'n'
        player.travel(random_exit)
        # the traversal_path is ultimately what matters, so append this direction to it. 
        # i.e. traversal_path = ['n']
        traversal_path.append(random_exit)
        # the temp_path is what matters right now, so append it there too. 
        # i.e. temp_path = ['n']
        temp_path.append(random_exit)
        # set a current pointer at the room the player is NOW in. this is a different room then where he/she was at the start of this loop
        new_current = player.current_room.id

        # check if this new room is already in the dictionary
        if new_current not in visited:
            # if it's not, set up a dictionary entry, much like we did with the last room before. essentially follow the same steps
            # i.e. visited = {'cur_room': {'n': '?', 'e':'?'}, 'new_current': {}}
            visited[new_current] = {}
            # get new room's connections to other rooms and put into an array called exits
            # i.e. exits = ['s', 'w']
            exits = player.current_room.get_exits()

            # for each of those unexplored connections
            for exit in exits:
                # assign it to a question mark, for the time being. 
                # i.e. visited = {'cur_room': {'n': '?', 'e':'?'}, 'new_current': {'s': '?', 'w': '?'}}
                visited[new_current][exit] = '?'

        # in the visited dictionary, override the question mark to map out connections 
        # i.e. visited = {'cur_room': {'n': 'new_current'},'new_current': {'s': '?'} }  
        visited[cur_room][random_exit] = new_current
        # make corresponding visited dictionary entry 
        # i.e. visited = {'cur_room':{'n': 'new_current'}, 'new_current': {'s': 'cur_room'}}  
        visited[new_current][reverse] = cur_room
        # add this new_current room to the queue so we can do this entire process over again
        q.enqueue(player.current_room.id)

    # the block below runs if there are NO unexplored connection to the room the player is currently in
    else:
        # pop off what's there and assign a pointer called direction 
        # i.e. direciton = 'n'
        direction = temp_path.pop()
        # find the reverse in the reference dictionary 
        # i.e. reverse = 's'
        reverse = retraced_steps[direction]
        # have the player travel in that direction. i.e. 's'
        player.travel(reverse)
        # as the traversal_path is ultimately what matters. add this 's' to the list
        traversal_path.append(reverse)
        # add this NEW room to the queue so we can do this entire process for this new room
        q.enqueue(player.current_room.id)



# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
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