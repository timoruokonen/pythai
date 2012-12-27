"""
@project: Pythai - Artificial Intellegence Project with Python
@package: Archon (Example game for AI)
@author: Timo Ruokonen (timoruokonen)
"""
import json

class archon:
    noMove = 0
    north = 1
    south = 2
    east = 3
    west = 4
    northwest = 5
    northeast = 6
    southwest = 7
    southeast = 8

    player_initial_energy = 100
    bullet_hit_energy = 60
    fire_timeout_in_rounds = 10
    player_speed = 3

    @staticmethod
    def get_next_location(x, y, direction):
        if (direction == archon.north):
            return [x, y - 1]
        if (direction == archon.south):
            return [x, y + 1]
        if (direction == archon.east):
            return [x + 1, y]
        if (direction == archon.west):
            return [x - 1, y]


class arena:

    width = 100
    height = 100

    def __init__(self):
        #create empty arena
        self.arena = [None] * arena.height
        for i in range(arena.height):
            self.arena[i] = [0] * arena.width

    def occupy(self, x, y, entity):
        if (x >= arena.width or x < 0 or y >= arena.height or y < 0):
            return False

        if not self.is_free(x, y):
            return False

        self.arena[x][y] = entity
        return True

    def clear(self, x, y):
        self.arena[x][y] = 0

    def is_free(self, x, y):
        return self.arena[x][y] == 0

    def get_item(self, x, y):
        #print "Get:", x, y
        if (self.out_of_bounds(x,y)):
            return None
        return self.arena[x][y]

    def out_of_bounds(self, x, y):
        if (x >= arena.width or x < 0 or y >= arena.height or y < 0):
            return True
        return False

    def peek(self, x, y, direction):
        distance = 0
        while True:
            next_location = archon.get_next_location(x, y, direction)
            x = next_location[0]
            y = next_location[1]

            if self.out_of_bounds(x, y):
                break
            
            if not self.is_free(x, y):
                break

            distance += 1
        
        #Now x,y is either out of the board or on some object...
        if self.out_of_bounds(x, y):
            return [0, distance]
        #print "(" + str(x) + ", " + str(y) + ") there is: " + str(self.arena[x][y]) 
        return [self.get_item(x, y), distance]

    def add_obstacle(self, x, y):
        obs = obstacle()
        obs.set_arena(self)
        obs.set_location(x, y)

    def print_ascii(self):
        for y in range(arena.height):
            row = ""
            for x in range(arena.width):
                if self.arena[x][y] == 0:
                    row += "."
                else:
                    row += "X"
            print row

class obstacle:
    def __init__(self):
        self.x = None
        self.y = None

    def set_arena(self, arena):
        self.arena = arena

    def set_location(self, x, y):
        self.x = x
        self.y = y
        self.arena.occupy(x, y, self)

    def hit(self, amount):
        pass
        #Obstacles are unbreakable!

class bullet:
    def __init__(self, arena, player, direction):
        self.arena = arena
        self.x = player.get_x()
        self.y = player.get_y()
        self.number = player.get_number()
        self.direction = direction
        self.flying = True
        self.first = True
        self.hit = None

    def advance(self):
        if not self.flying:
            return

        next_location = archon.get_next_location(self.x, self.y, self.direction)
        if self.arena.out_of_bounds(next_location[0], next_location[1]):
            self.flying = False
            self.arena.clear(self.x, self.y)
            return

        if self.arena.occupy(next_location[0], next_location[1], self):
            if not self.first:
                self.arena.clear(self.x, self.y)
            self.first = False
            #print "moved to ", next_location[0], next_location[1]
        else:
            self.flying = False
            self.hit = self.arena.get_item(next_location[0], next_location[1])
            self.arena.clear(self.x, self.y)

        self.x = next_location[0]
        self.y = next_location[1]
        
    def get_hit(self):
        return self.hit

    def is_flying(self):
        return self.flying

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

class game:
    def __init__(self):
        self.players = list()
        self.bullets = list()

    def set_arena(self, arena):
        self.arena = arena

    def add_player(self, player):
        self.players.append(player)
        player.set_game(self)
        
    def advance(self):
        #update players
        for player in self.players:
            player.update()

        #avance bullets
        bullets_copy = self.bullets
        for bullet in bullets_copy:
            bullet.advance()
            if not bullet.flying:
                #handle bullet hit
                target = bullet.get_hit() 
                if (target != None):
                    print "Bullet hit!! " + str(target)
                    #print "Target is: " + str(target)
                    target.hit(archon.bullet_hit_energy)
                self.bullets.remove(bullet)
        
    def add_bullet(self, player, direction):
        b = bullet(self.arena, player, direction)
        self.bullets.append(b) 

    def get_status_json(self):
        status = {}
        
        players = []
        for player in self.players:
            players.append({"id": player.get_number(), "x": player.get_x(), "y": player.get_y() });
        status["players"] = players;

        return json.dumps(status)

            


class player:

    def __init__(self, number):
        self.x = None
        self.y = None
        self.number = number
        self.energy = archon.player_initial_energy

        self.last_fired_timeout = 0

        self.turn_used = False
        
        self.move_timeout = 0
        self.direction = None

    def set_arena(self, arena):
        self.arena = arena

    def set_game(self, game):
        self.game = game

    def set_location(self, x, y):
        self.x = x
        self.y = y
        self.arena.occupy(x, y, self)

    def update(self):
        if (self.last_fired_timeout > 0):
            self.last_fired_timeout -= 1
        self.turn_used = False

        self._update_movement()

    def is_dead(self):
        return self.energy < 0

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_number(self):
        return self.number

    def get_energy(self):
        return self.energy

    def hit(self, amount):
        self.energy -= amount
        if (self.energy < 0):
            print str(self) + " is DEAD!"

    def fire(self, direction):
        if (not self.turn_used and self.last_fired_timeout <= 0):
            self.game.add_bullet(self, direction)
            self.last_fired_timeout = archon.fire_timeout_in_rounds
            self.turn_used = True

    def move(self, direction):
        if (self.turn_used):
            return False

        if (direction == archon.noMove):
            self.direction = None
            return True    
        
        next_location = archon.get_next_location(self.x, self.y, direction)
        if self.arena.get_item(next_location[0], next_location[1]) != 0:
            self.direction = None
            return False

        if (self.direction != direction):
            self.direction = direction            
            self.turn_used = True    
            self.move_timeout = archon.player_speed
        return True

    def _update_movement(self):
        if (self.direction == None):
            return 
        self.move_timeout -= 1
        if (self.move_timeout > 0):
            return

        next_location = archon.get_next_location(self.x, self.y, self.direction)
        #print "Trying to move: ", next_location[0], next_location[1]
        if self.arena.occupy(next_location[0], next_location[1], self):
            self.arena.clear(self.x, self.y)
            self.x = next_location[0]
            self.y = next_location[1]
            #self.turn_used = True
        self.move_timeout = archon.player_speed

    def __str__(self):
        return "Player " + str(self.number) + ", Energy: " + str(self.energy)


if __name__ == '__main__':
    arena = arena()
    p = player(1)
    p.set_arena(arena)
    p.set_location(0,0)
    p2 = player(2)
    p2.set_arena(arena)
    p2.set_location(3,6)

    #print arena.arena[0][0]
    #print arena.arena[arena.height - 1][arena.width - 1]
    while (p.move(archon.south)):
        pass
    while (p.move(archon.east)):
        arena.peek(p.x, p.y, archon.north)
        print "peek north: ", arena.peek(p.x, p.y, archon.north)[0], " dist: ", arena.peek(p.x, p.y, archon.north)[1] 
        pass
    print "Player moved to: ", p.x, ", ", p.y

    arena.print_ascii()





    
