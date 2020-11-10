from datetime import date

from django.contrib.auth import get_user_model
from django.db import connection, models
from django.utils import timezone


class Post(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def aggregate_post_likes(self, date_from: date, date_to: date):
        diffence_in_days = (date_to - date_from).days

        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT d.date, count(pl.id)
                FROM (
                        SELECT to_char(date_trunc('day', (to_date(%(date_to)s, 'YYYY-MM-DD') - offs)), 'YYYY-MM-DD') AS date
                        FROM generate_series(0, %(difference)s, 1) AS offs
                    ) d LEFT OUTER JOIN
                    {PostLike._meta.db_table} AS pl
                    ON d.date = to_char(date_trunc('day', pl.date_created), 'YYYY-MM-DD') 

                GROUP BY d.date ORDER BY d.date;
                """,
                {
                    "date_to": date_to.isoformat(),
                    "difference": diffence_in_days,
                    "post_id": self.pk,
                },
            )

            return {date: total_likes for date, total_likes in cursor.fetchall()}


class PostLike(models.Model):
    post = models.ForeignKey(
        "Post",
        on_delete=models.CASCADE,
        related_name="likes",
        related_query_name="like",
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="post_likes",
        related_query_name="post_like",
    )

    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = (("user", "post"),)
