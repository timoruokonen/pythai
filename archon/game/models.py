from django.db import models

class Game(models.Model):
    string = ""	

    def __unicode__(self):
        return self.string

#class Choice(models.Model):
#    poll = models.ForeignKey(Poll)
#    choice_text = models.CharField(max_length=200)
#    votes = models.IntegerField()
