from django.db import models
from django.db.models import Sum


class Paperboy(models.Model):
    name = models.CharField(max_length=200)
    experience = models.IntegerField(default=0)
    earnings = models.FloatField(default=0.0)

    def __str__(self):
        return "Paperboy {}: {}".format(self.id, self.name)

    def calculate_pay(self, houses_delivered):
        pay = 0.25 * houses_delivered

        if houses_delivered > self.quota():
            pay += 0.25 * (houses_delivered - self.quota())
        elif houses_delivered < self.quota():
            pay -= 2

        return pay

    def deliver(self, address1, address2):
        houses = address2 - address1 + 1
        pay = self.calculate_pay(houses)
        self.earnings += pay
        self.experience += houses
        self.save()
        return pay

    def quota(self):
        return 50 + self.experience * 0.5

    @classmethod
    def total_earnings(cls):
        if Paperboy.objects.exists():
            return Paperboy.objects.aggregate(Sum('earnings'))['earnings__sum']
        else:
            return 0

    @classmethod
    def total_papers(cls):
        if Paperboy.objects.exists():
            return Paperboy.objects.aggregate(Sum('experience'))['experience__sum']
        else:
            return 0

    def report(self):
        return "Hi, my name is {}. I have delivered {} papers so far and earned ${}.".format(self.name, self.experience, self.earnings)
