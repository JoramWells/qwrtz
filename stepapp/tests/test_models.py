from django.test import TestCase
from stepapp.models import Post

class TestModels(TestCase):
    def setUp(self):
        self.post1 = Post.objects.create(
            keyword="monday",
            # min_video=2,
            created_on="2021-02-10"
        )
