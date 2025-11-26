
from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone
from django.conf import settings
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'


    def handle(self, *args, **kwargs):
        # Drop collections directly to avoid orphaned/malformed documents
        client = MongoClient('localhost', 27017)
        db = client[settings.DATABASES['default']['NAME']]
        for col in ['users', 'teams', 'activities', 'leaderboards', 'workouts']:
            db[col].drop()
        client.close()

        # Create Teams
        marvel = Team.objects.create(name='Team Marvel', universe='Marvel')
        dc = Team.objects.create(name='Team DC', universe='DC')

        # Create Users (Superheroes)
        users = [
            User.objects.create(name='Spider-Man', email='spiderman@marvel.com', team=marvel),
            User.objects.create(name='Iron Man', email='ironman@marvel.com', team=marvel),
            User.objects.create(name='Wonder Woman', email='wonderwoman@dc.com', team=dc),
            User.objects.create(name='Batman', email='batman@dc.com', team=dc),
        ]

        # Create Workouts
        workouts = [
            Workout.objects.create(name='Super Strength', description='Strength training for superheroes', difficulty='Hard'),
            Workout.objects.create(name='Agility Training', description='Improve agility and reflexes', difficulty='Medium'),
        ]

        # Create Activities
        Activity.objects.create(user=users[0], type='Web Swinging', duration=30, date=timezone.now().date())
        Activity.objects.create(user=users[1], type='Suit Upgrade', duration=45, date=timezone.now().date())
        Activity.objects.create(user=users[2], type='Lasso Practice', duration=40, date=timezone.now().date())
        Activity.objects.create(user=users[3], type='Detective Work', duration=60, date=timezone.now().date())

        # Create Leaderboard
        Leaderboard.objects.create(user=users[0], score=100, rank=1)
        Leaderboard.objects.create(user=users[1], score=90, rank=2)
        Leaderboard.objects.create(user=users[2], score=85, rank=3)
        Leaderboard.objects.create(user=users[3], score=80, rank=4)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
