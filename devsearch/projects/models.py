from django.db import models
from users.models import Profile


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    featured_image = models.ImageField(default="default.jpg", upload_to="projects/%Y/%m/%d/")
    demo_link = models.CharField(max_length=2000, blank=True)
    source_link = models.CharField(max_length=2000, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    vote_total = models.IntegerField(default=0)
    vote_ratio = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-vote_ratio', '-vote_ratio', 'title']

    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

    def get_vote_count(self):
        reviews = self.review_set.all()
        up_votes = reviews.filter(value='up').count()
        total_votes = reviews.count()

        ratio = up_votes / total_votes * 100
        self.vote_total = total_votes
        self.vote_ratio = ratio

        self.save()

class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'UP Vote'),
        ('down', 'Down Vote'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(blank=True)
    value = models.CharField(max_length=50, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.value

    class Meta:
        unique_together = [['owner', 'project']]
