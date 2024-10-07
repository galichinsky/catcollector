from django.db import models
from django.urls import reverse

from django.contrib.auth.models import User

MEALS = (("B", "Breakfast"), ("L", "Lunch"), ("D", "Dinner"))

# Create your models here.


class Toy(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("toy-detail", kwargs={"pk": self.id})


class Cat(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    # M:M relationship with toys
    toys = models.ManyToManyField(Toy)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.id})"

    def get_absolute_url(self):
        return reverse("cat-detail", kwargs={"cat_id": self.id})


class Feeding(models.Model):
    date = models.DateField("Feeding date")
    meal = models.CharField(max_length=1, choices=MEALS, default=MEALS[0][0])
    # The "many"/"child" side of the 1:M relationship must always have a ForeignKey field
    # There will be a cat_id column/table in the database
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_meal_display()} on {self.date}"

    class Meta:
        ordering = ["-date"]  # Sort feedings in descending order by date
