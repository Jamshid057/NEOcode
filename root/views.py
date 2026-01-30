from django.db.models import Count, Q
from django.shortcuts import render

from problems.models import Category


def HomePageView(request):
    categories = Category.objects.annotate(
        difficult_count=Count("problem", filter=Q(problem__stars=True))
    )
    for c in categories:
        c.star_range = range(c.difficult_count)

    return render(
        request,
        "home.html",
        context={"categories": categories},
    )
