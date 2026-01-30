from django.contrib import admin

from .models import Category, Problem, TestCase


class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 1
    fields = ("input_data", "expected_output", "order", "is_sample")
    ordering = ("order",)


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "function_name", "stars")
    list_filter = ("category", "stars")
    search_fields = ("title", "function_name")
    inlines = [TestCaseInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ("problem", "order", "input_data_short", "expected_output_short", "is_sample")
    list_filter = ("problem__category", "is_sample")
    list_editable = ("order", "is_sample")
    search_fields = ("problem__title",)
    ordering = ("problem", "order")

    def input_data_short(self, obj):
        s = (obj.input_data or "")[:50]
        return s + "…" if len(obj.input_data or "") > 50 else s

    input_data_short.short_description = "Input"

    def expected_output_short(self, obj):
        s = (obj.expected_output or "")[:30]
        return s + "…" if len(obj.expected_output or "") > 30 else s

    expected_output_short.short_description = "Expected"
