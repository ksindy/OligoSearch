from django.db import models

class conversions(models.Model):
    sequence_input = models.TextField()
    pattern_input = models.TextField()

    def __str__(self):
        return '%s' % (self.sequence,)
