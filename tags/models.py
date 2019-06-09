from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

    def num_topics(self):
        return len(self.topic_set.all())
