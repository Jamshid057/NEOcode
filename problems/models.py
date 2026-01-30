from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Problem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    stars = models.BooleanField(default=False)
    function_name = models.CharField(max_length=255)
    params = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Problem"
        verbose_name_plural = "Problems"

    def __str__(self):
        return self.title


class TestCase(models.Model):

    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        related_name="test_cases",
    )
    input_data = models.TextField(help_text="Vergul bilan ajratilgan: 10, 20")
    expected_output = models.TextField(help_text="Kutilgan natija (string)")
    order = models.PositiveIntegerField(default=0, help_text="Tartib raqami")
    is_sample = models.BooleanField(
        default=False,
        help_text="Ha bo'lsa, masala sahifasida namuna sifatida ko'rsatiladi",
    )

    class Meta:
        verbose_name = "Test case"
        verbose_name_plural = "Test cases"
        ordering = ["order", "pk"]

    def __str__(self):
        return f"{self.problem.title} — #{self.order}"
