from django.contrib import admin

from .models import Submission


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("user", "problem", "solved_at")
    list_filter = ("problem__category",)
    search_fields = ("user__email", "problem__title")
    ordering = ("-solved_at",)
