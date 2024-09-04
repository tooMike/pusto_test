from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Player(models.Model):
    """Модель игрока."""

    user = models.OneToOneField(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        related_name="player"
    )
    first_enter = models.DateTimeField(
        verbose_name="Время первого входа",
        null=True,
        blank=True
    )
    last_enter = models.DateTimeField(
        verbose_name="Время последнего входа",
        null=True,
        blank=True
    )
    bonuses = models.ManyToManyField(
        "Boost",
        through="Bonus",
        verbose_name="Бонусы",
        related_name="players"
    )

    class Meta:
        verbose_name = "игрок"
        verbose_name_plural = "Игроки"

    def add_bonus(self, boost, amount):
        """Добавление игроку бонуса."""
        if amount < 1:
            raise ValueError("Количество не может быть меньше 1.")
        bonus, created = Bonus.objects.get_or_create(
            player=self,
            boost=boost,
        )
        bonus.amount += amount
        bonus.save()


class Boost(models.Model):
    """Модель бустов."""

    name = models.CharField(verbose_name="Название", max_length=100)
    boost_type = models.CharField(verbose_name="Тип", max_length=100)

    class Meta:
        verbose_name = "буст"
        verbose_name_plural = "Бусты"
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'boost_type'],
                name='unique_boost'
            )
        ]


class Bonus(models.Model):
    """Модель бонусов (связь игрока и бустров)."""

    player = models.ForeignKey(
        Player,
        verbose_name="Игрок",
        on_delete=models.CASCADE,
        related_name="bonus_entries"
    )
    boost = models.ForeignKey(
        Boost,
        verbose_name="Буст",
        on_delete=models.CASCADE,
        related_name="bonus_boosts"
    )
    awarded_at = models.DateTimeField(
        verbose_name="Дата добавления",
        auto_now_add=True
    )
    amount = models.IntegerField(
        verbose_name="Количество",
        default=1,
        validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = "бонус"
        verbose_name_plural = "бонусы"
        constraints = [
            models.UniqueConstraint(
                fields=["player", "boost"], name="unique_bonus"
            )
        ]
