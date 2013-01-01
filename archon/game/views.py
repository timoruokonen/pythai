"""
@project: Pythai - Artificial Intellegence Project with Python
@package: Archon (Example game for AI)
@author: Satu Suuronen (satusuuronen)
"""


from django.http import HttpResponse
from django.template import Context, loader
from game.models import Game
from archon import *
import threading


class gameWrapper:
    _instance = None

    def __init__(self):
        self.a = arena()
        self.p1 = player(0)
        self.p2 = player(1)
        self.p1.set_arena(self.a)
        self.p2.set_arena(self.a)
        self.p1.set_location(20,20)
        self.p2.set_location(5,5)
        self.p1.ai = ai(self.p1)
        self.p2.ai = None
        self.command_lock = threading.Lock()

        self.game = game()
        self.game.set_arena(self.a)
        self.game.add_player(self.p1)
        self.game.add_player(self.p2)


    @staticmethod
    def instance():
        if gameWrapper._instance == None:
            gameWrapper._instance = gameWrapper()
        return gameWrapper._instance

    @staticmethod
    def reset():
        gameWrapper._instance = None

def shoot(request, id):
    wrapper = gameWrapper.instance()
    wrapper.command_lock.acquire()
    resp = int(request.GET.get('dir'))
    wrapper.p2.fire(resp)
    wrapper.command_lock.release()
    return HttpResponse(resp)
		
def move(request, id):
    wrapper = gameWrapper.instance()
    resp = int(request.GET.get('dir'))
    wrapper.p2.move(resp)
    return HttpResponse(resp)

def index(request):
    t = loader.get_template('game/index.html')
    c = Context()
    return HttpResponse(t.render(c))
    

def status(request):
    wrapper = gameWrapper.instance()
    wrapper.command_lock.acquire()
    resp = wrapper.game.get_status_json()
    wrapper.game.advance()
    wrapper.command_lock.release()
    return HttpResponse(resp)

def reset(request):
    gameWrapper.reset()
    return HttpResponse()




    
    
