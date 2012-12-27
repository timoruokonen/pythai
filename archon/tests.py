"""
@project: Pythai - Artificial Intellegence Project with Python
@package: Archon (Example game for AI)
@author: Timo Ruokonen (timoruokonen)
"""

from archon import *
import unittest

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.seq = range(10)
        self.a = arena()
        self.p1 = player(1)
        self.p2 = player(2)
        self.p1.set_arena(self.a)
        self.p2.set_arena(self.a)
        self.p1.set_location(0,0)

        self.game = game()
        self.game.set_arena(self.a)
        self.game.add_player(self.p1)
        self.game.add_player(self.p2)
        
        self.max_x = arena.width - 1
        self.max_y = arena.height - 1

    def advance_game(self, rounds):
        for i in range(rounds):
            self.game.advance()

    def test_move_one_player(self):
        while (self.p1.move(archon.south)):
            self.advance_game(1)
        
        self.assertEqual(0, self.p1.get_x())            
        self.assertEqual(self.max_y, self.p1.get_y())            
        while (self.p1.move(archon.east)):
            self.advance_game(1)

        self.assertEqual(self.max_x, self.p1.get_x())        
        self.assertEqual(self.max_y, self.p1.get_y())

        self.p1.move(archon.north)
        self.advance_game(archon.player_speed)
        self.p1.move(archon.north)
        self.advance_game(archon.player_speed)
        self.p1.move(archon.west)
        self.advance_game(archon.player_speed)
        self.p1.move(archon.north)
        self.advance_game(archon.player_speed)
        self.p1.move(archon.west)
        self.advance_game(archon.player_speed)
        self.p1.move(archon.east)
        self.advance_game(archon.player_speed)
        self.p1.move(archon.south)
        self.advance_game(archon.player_speed)
        self.assertEqual(self.max_x - 1, self.p1.get_x())        
        self.assertEqual(self.max_y - 2, self.p1.get_y())


    def test_move_inbounds(self):
        self.assertFalse(self.p1.move(archon.west))
        self.assertEqual(0, self.p1.get_x())        
        self.assertEqual(0, self.p1.get_y())
        self.assertFalse(self.p1.move(archon.north))
        self.assertEqual(0, self.p1.get_x())        
        self.assertEqual(0, self.p1.get_y())
        self.p1.set_location(self.max_x, self.max_y)
        self.assertFalse(self.p1.move(archon.east))
        self.assertEqual(self.max_x, self.p1.get_x())        
        self.assertEqual(self.max_y, self.p1.get_y())
        self.assertFalse(self.p1.move(archon.south))
        self.assertEqual(self.max_x, self.p1.get_x())        
        self.assertEqual(self.max_y, self.p1.get_y())

    def test_move_over_other_player(self):
        self.p1.set_location(1,1)
        self.p2.set_location(1,2)
        self.assertFalse(self.p2.move(archon.north))
        self.assertEqual(2, self.p2.get_y())        
        self.assertFalse(self.p1.move(archon.south))
        self.assertEqual(1, self.p1.get_y())        
   
        self.p1.set_location(3,3)
        self.p2.set_location(4,3)
        self.assertFalse(self.p2.move(archon.west))
        self.assertEqual(4, self.p2.get_x())        
        self.assertFalse(self.p1.move(archon.east))
        self.assertEqual(3, self.p1.get_x())        

    def test_game_fire_bullet(self):
        self.p1.fire(archon.south)
        self.assertEqual(1, len(self.game.bullets)) 
        self.advance_game(self.max_y + 1)
        self.assertEqual(0, len(self.game.bullets)) 
        self.assertEqual(0, self.a.get_item(0, self.max_y)) 

        self.advance_game(archon.fire_timeout_in_rounds)        
        self.p1.fire(archon.north)
        self.assertEqual(1, len(self.game.bullets)) 
        self.advance_game(1)
        self.assertEqual(0, len(self.game.bullets)) 

        self.advance_game(archon.fire_timeout_in_rounds)        
        self.p1.move(archon.east)
        self.advance_game(archon.player_speed)        
        self.p1.fire(archon.west)
        self.assertEqual(1, len(self.game.bullets)) 
        self.advance_game(1)
        self.assertEqual(1, len(self.game.bullets)) 
        self.advance_game(1)
        self.assertEqual(0, len(self.game.bullets))  

    def test_game_fire_bullet_and_hit(self):
        self.p1.set_location(3,1)
        self.p2.set_location(3,4)

        #player 1 shoots player 2
        self.p1.fire(archon.south)
        self.advance_game(2)
        self.assertEqual(1, len(self.game.bullets))
        self.assertEqual(archon.player_initial_energy, self.p2.get_energy()) 
        self.advance_game(1)
        self.assertEqual(0, len(self.game.bullets)) 
        self.assertEqual(archon.player_initial_energy - archon.bullet_hit_energy, self.p2.get_energy()) 
        self.assertFalse(self.p2.is_dead())
        self.assertEqual(self.p1, self.a.get_item(3, 1))
        self.assertEqual(self.p2, self.a.get_item(3, 4))
        
        #advance game and check that nothing happens...
        self.advance_game(50)
        self.assertEqual(0, len(self.game.bullets)) 
        self.assertEqual(archon.player_initial_energy - archon.bullet_hit_energy, self.p2.get_energy()) 
        self.assertFalse(self.p2.is_dead())

        #kill the player 2 by shooting again
        self.p1.fire(archon.south)
        self.advance_game(3)
        self.assertEqual(0, len(self.game.bullets)) 
        self.assertEqual(archon.player_initial_energy -  2 * archon.bullet_hit_energy, self.p2.get_energy()) 
        self.assertTrue(self.p2.is_dead())

    def test_game_fire_bullet_and_hit_both_ways(self):
        self.p1.set_location(3,1)
        self.p2.set_location(3,4)

        #player 1 shoots player 2
        self.p1.fire(archon.south)
        self.advance_game(10)
        self.assertEqual(archon.player_initial_energy - archon.bullet_hit_energy, self.p2.get_energy()) 
        self.assertFalse(self.p2.is_dead())
        
        #player 2 "moves" to another location and shoots player 1
        self.p2.set_location(5, 1)
        self.p2.fire(archon.west)
        self.advance_game(10)
        self.assertEqual(archon.player_initial_energy - archon.bullet_hit_energy, self.p1.get_energy()) 
        self.assertFalse(self.p1.is_dead())

        #player 1 shoots and misses
        self.p1.fire(archon.west)
        self.advance_game(10)

        #player 2 kills player 1 by shooting again
        self.p2.fire(archon.west)
        self.advance_game(10)
        self.assertEqual(archon.player_initial_energy -  2 * archon.bullet_hit_energy, self.p1.get_energy()) 
        self.assertTrue(self.p1.is_dead())

    def test_game_fire_bullet_and_dodge(self):
        p1_start_x = 2 + archon.player_speed + 1
        self.p1.set_location(p1_start_x, 1)
        self.p2.set_location(2, 1)

        #player 1 shoots player 2
        self.p1.fire(archon.west)
        self.advance_game(1)
        self.assertEqual(archon.player_initial_energy, self.p2.get_energy()) 
        self.assertEqual(1, len(self.game.bullets))
        self.assertTrue(isinstance(self.a.get_item(p1_start_x - 1, 1), bullet))
        
        #player 2 dodges
        self.p2.move(archon.south)
        self.advance_game(archon.player_speed)
        self.assertEqual(archon.player_initial_energy, self.p2.get_energy()) 
        self.assertEqual(1, len(self.game.bullets))
        self.assertTrue(isinstance(self.a.get_item(2, 1), bullet))

        #bullet continues flying until hits the wall
        self.advance_game(2)
        self.assertEqual(1, len(self.game.bullets))
        self.advance_game(1)
        self.assertEqual(0, len(self.game.bullets))
        self.assertEqual(archon.player_initial_energy, self.p2.get_energy()) 

    def test_player_fires_before_fire_timeout_is_passed(self):
        self.p1.fire(archon.south)
        self.advance_game(1)
        self.assertEqual(1, len(self.game.bullets))
        self.assertTrue(isinstance(self.a.get_item(0,1), bullet))
        
        self.p1.fire(archon.south)
        self.advance_game(1)
        self.assertEqual(1, len(self.game.bullets))

        self.advance_game(archon.fire_timeout_in_rounds - 3)
        current_number_of_bullets = len(self.game.bullets) 
        self.p1.fire(archon.south)
        self.assertEqual(current_number_of_bullets, len(self.game.bullets))

        self.advance_game(1)
        current_number_of_bullets = len(self.game.bullets) 
        self.p1.fire(archon.south)
        self.assertEqual(current_number_of_bullets + 1, len(self.game.bullets))
        self.advance_game(1)
        self.assertTrue(isinstance(self.a.get_item(0,1), bullet))
        
    def test_player_cannot_fire_and_move_on_same_turn(self):
        #fire first and then try to move
        self.p1.fire(archon.south)
        self.assertFalse(self.p1.move(archon.east))
        self.advance_game(archon.player_speed)
        self.assertEqual(0, self.p1.get_x())        
        self.assertEqual(0, self.p1.get_y())
        self.assertEqual(1, len(self.game.bullets))
        self.assertTrue(isinstance(self.a.get_item(0,archon.player_speed), bullet))

        #move first and then try to move
        self.p2.set_location(4,4)
        self.assertTrue(self.p2.move(archon.north))
        self.p2.fire(archon.north)
        self.advance_game(archon.player_speed)
        self.assertEqual(4, self.p2.get_x())        
        self.assertEqual(3, self.p2.get_y())
        self.assertEqual(1, len(self.game.bullets))

    def test_player_cannot_hit_own_bullet(self):
        self.p1.fire(archon.south)
        self.advance_game(1)
        self.assertFalse(self.p1.move(archon.south))
        self.advance_game(1)
        self.assertTrue(self.p1.move(archon.south))
        self.advance_game(archon.player_speed)

        self.assertEqual(1, self.p1.get_y())
        self.assertEqual(1, len(self.game.bullets))
        self.assertTrue(isinstance(self.a.get_item(0, 2 + archon.player_speed), bullet))


    def test_game_player_cannot_move_through_obstacle(self):
        self.a.add_obstacle(1,1)

        #try to move through object from top
        self.p1.move(archon.east)
        self.advance_game(archon.player_speed)
        self.assertEqual(1, self.p1.get_x())        
        self.assertEqual(0, self.p1.get_y())
        self.assertFalse(self.p1.move(archon.south))
        self.advance_game(archon.player_speed)
        self.assertEqual(1, self.p1.get_x())        
        self.assertEqual(0, self.p1.get_y())

        #try to move through object from right
        self.p1.move(archon.east)
        self.advance_game(archon.player_speed)
        self.p1.move(archon.south)
        self.advance_game(archon.player_speed)
        self.assertEqual(2, self.p1.get_x())        
        self.assertEqual(1, self.p1.get_y())
        self.assertFalse(self.p1.move(archon.west))
        self.advance_game(archon.player_speed)
        self.assertEqual(2, self.p1.get_x())        
        self.assertEqual(1, self.p1.get_y())

        #try to move through object from below
        self.p1.move(archon.south)
        self.advance_game(archon.player_speed)
        self.p1.move(archon.west)
        self.advance_game(archon.player_speed)
        self.assertEqual(1, self.p1.get_x())        
        self.assertEqual(2, self.p1.get_y())
        self.assertFalse(self.p1.move(archon.north))
        self.advance_game(archon.player_speed)
        self.assertEqual(1, self.p1.get_x())        
        self.assertEqual(2, self.p1.get_y())

        #try to move through object from left
        self.p1.move(archon.west)
        self.advance_game(archon.player_speed)
        self.p1.move(archon.north)
        self.advance_game(archon.player_speed)
        self.assertEqual(0, self.p1.get_x())        
        self.assertEqual(1, self.p1.get_y())
        self.assertFalse(self.p1.move(archon.east))
        self.advance_game(archon.player_speed)
        self.assertEqual(0, self.p1.get_x())        
        self.assertEqual(1, self.p1.get_y())

    def test_game_bullet_is_blocked_by_obstacle(self):
        self.a.add_obstacle(3,3)
        self.p1.set_location(3,1)
        self.p2.set_location(3,4)

        #player 1 shoots obstacle
        self.p1.fire(archon.south)
        self.advance_game(10)
        self.assertEqual(0, len(self.game.bullets)) 
        self.assertEqual(archon.player_initial_energy, self.p2.get_energy()) 
        self.assertFalse(self.p2.is_dead())

        #player 1 shoots obstacle when being next to it
        self.p1.move(archon.south)
        self.advance_game(archon.player_speed)
        self.p1.fire(archon.south)
        self.advance_game(1)
        self.assertEqual(0, len(self.game.bullets)) 

    def test_game_status_json(self):
        self.p2.set_location(6,2)
        print self.game.get_status_json()

    def test_move_and_stop_player(self):
        self.p1.move(archon.south)
        self.advance_game(archon.player_speed)
        self.advance_game(archon.player_speed)
        self.assertEqual(0, self.p1.get_x())        
        self.assertEqual(2, self.p1.get_y())
        self.p1.move(archon.noMove)
        self.advance_game(archon.player_speed)
        self.assertEqual(0, self.p1.get_x())        
        self.assertEqual(2, self.p1.get_y())




if __name__ == '__main__':
    unittest.main()

