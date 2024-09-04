import csv
import os
import shutil

from django.apps import apps
from django.core.management.base import BaseCommand

triples = [
    "levels:Player:data/player.csv",
    "levels:Level:data/level.csv",
    "levels:Prize:data/prize.csv",
    "levels:PlayerLevel:data/player_level.csv",
    "levels:LevelPrize:data/level_prize.csv",
    "levels:PlayerLevelPrize:data/player_level_prize.csv",
]


class Command(BaseCommand):
    help = (
        "Загрузка данных из csv-файлов в модели. ",
        "Пример команды: python manage.py import_data ",
    )

    def handle(self, *args, **options):

        for triple in triples:
            parts = triple.split(":")
            if len(parts) == 3:
                app_name, model_name, csv_file_path = parts
                model = apps.get_model(app_name, model_name)
                self.import_data(model, csv_file_path)
            else:
                self.stdout.write(
                    self.style.ERROR(f"Неверный формат: '{triple}'")
                )

    def copy_file(self, src_file, dest_dir):
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        dest_path = os.path.join(dest_dir, os.path.basename(src_file))
        shutil.copy2(src_file, dest_path)
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully copied {src_file} to {dest_path}"
            )
        )

    def import_data(self, model, csv_file_path):
        with open(csv_file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            field_names = next(reader)  # Получение заголовков
            for row in reader:
                data = {
                    field_names[i]: row[i] for i in range(len(field_names))
                }
                # Распаковываем словарь и создаем объект модели если его еще
                # нет в БД
                if not model.objects.filter(**data).exists():
                    model.objects.create(**data)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully imported data {model}")
        )
