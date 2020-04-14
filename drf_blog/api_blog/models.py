from django.db import models
from rest_framework.reverse import reverse




class BlogPost(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title   = models.CharField(max_length=100, blank=True, default='')
    content = models.TextField(max_length=120, null=True, blank=True)
    like    = models.SmallIntegerField(null=True, blank=True)
    unlike  = models.SmallIntegerField(null=True, blank=True)
    owner   = models.ForeignKey('auth.User',
                                related_name='blogposts',
                                on_delete=models.CASCADE
                                )

    class Meta:
        ordering = ['created']

    def get_api_url(self, request=None):
        return reverse("blogpost-detail", kwargs={'pk': self.pk})
