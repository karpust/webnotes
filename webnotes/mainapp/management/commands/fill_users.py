import os
import json
from django.core.management.base import BaseCommand
from authapp.models import User

JSON_PATH = './mainapp/json'


def load_from_json(f_name):
    with open(os.path.join(JSON_PATH, f_name + '.json'), 'r', encoding='utf-8') as f:
        return json.load(f)


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = load_from_json('users')
        User.objects.all().delete()
        new_user = User(**users)
        new_user.save()

        super_user = User.objects.create_superuser(
            'admin', 'djangodrf@mail.ru', 'superdrf')

