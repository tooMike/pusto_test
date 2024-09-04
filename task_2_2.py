import csv

from django.http import StreamingHttpResponse

from levels.models import PlayerLevel


class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def export_player_levels_to_csv(request):
    """Выгрузка данных об игроках и уровнях в формате CSV."""

    # Выгружаем из БД необходимые данные
    player_levels = PlayerLevel.objects.select_related(
        "level"
    ).prefetch_related(
        "level__level_prize__prize"
    ).values(
        "player_id",
        "level__title",
        "is_completed",
        "level__level_prize__prize__title"
    )

    # Формируем строки для записи в файл
    rows = (
        [
            player_level["player_id"],
            player_level["level__title"],
            player_level["is_completed"],
            player_level["level__level_prize__prize__title"] if player_level[
                "is_completed"] else "Приз отсутствует",
        ] for player_level in player_levels
    )
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    return StreamingHttpResponse(
        (writer.writerow(row) for row in rows),
        content_type="text/csv",
        headers={
            "Content-Disposition": "attachment; "
                                   "filename=player_levels_result.csv"
        },
    )
