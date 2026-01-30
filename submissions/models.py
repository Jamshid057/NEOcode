from django.conf import settings
from django.db import models


class Submission(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="submissions",
    )
    problem = models.ForeignKey(
        "problems.Problem",
        on_delete=models.CASCADE,
        related_name="submissions",
    )
    solved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Submission"
        verbose_name_plural = "Submissions"
        unique_together = [["user", "problem"]]

    def __str__(self):
        return f"{self.user} — {self.problem.title}"
