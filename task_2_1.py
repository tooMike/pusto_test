from django.db import models
from django.utils import timezone


class Player(models.Model):
    """Модель игрока."""

    player_id = models.CharField(max_length=100)


class Level(models.Model):
    """Модель уровня."""

    title = models.CharField(max_length=100)
    order = models.IntegerField(default=0)


class Prize(models.Model):
    """Модель приза."""

    title = models.CharField(max_length=100)


class PlayerLevel(models.Model):
    """Модель для связи игрока и его уровня."""

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    completed = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)

    def complete_level(self):
        """Завершение уровня и присвоение приза игроку за его прохождение."""

        # Проверяем, не был ли уровень уже завершен
        if self.is_completed:
            raise ValueError("Этот уровень уже был завершен.")

        # Получаем приз для данного уровня
        level_prize = LevelPrize.objects.filter(level=self.level).first()
        # Присваиваем приз, если он существует
        if level_prize:
            player_prize, created = PlayerLevelPrize.objects.get_or_create(
                player=self.player,
                level_prize=level_prize
            )
            if not created:
                raise ValueError(
                    "Игрок уже получил этот приз."
                )

        # Обновляем информацию о прохождении
        self.completed = timezone.now().date()
        self.is_completed = True
        self.save()


class LevelPrize(models.Model):
    """
    Модель для связи уровней и призов.

    Из модели убрано поле received, так как эта модель не связана с конкретным
    игроком. Для реализации этой связи добавлена модель PlayerLevelPrize,
    которая связываем конкретный приз за уровень с игроком.
    """

    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE)
    # received = models.DateField()

    class Meta:
        default_related_name = "level_prize"


class PlayerLevelPrize(models.Model):
    """Модель для связи игрока и полученного приза за уровень."""

    player = models.ForeignKey(
        Player,
        verbose_name="Игрок",
        on_delete=models.CASCADE,
    )
    level_prize = models.ForeignKey(
        LevelPrize,
        verbose_name="Приз за уровень",
        on_delete=models.CASCADE,
    )
    received_at = models.DateTimeField(
        verbose_name="Дата получения приза",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "приз игрока"
        verbose_name_plural = "Призы игроков"
        default_related_name = "player_level_prize"
        constraints = [
            models.UniqueConstraint(
                fields=["player", "level_prize"], name="unique_prize"
            )
        ]
