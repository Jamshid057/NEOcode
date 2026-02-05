from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import Category, Problem
from submissions.models import Submission


def category_problem_list(request, pk):
    category = get_object_or_404(Category, pk=pk)
    problems = Problem.objects.filter(category=category).order_by("pk")

    solved_problem_ids = set()
    if request.user.is_authenticated:
        solved_problem_ids = set(
            Submission.objects.filter(user=request.user).values_list(
                "problem_id", flat=True
            )
        )

    return render(
        request,
        "problems/problem_list.html",
        context={
            "category": category,
            "problems": problems,
            "solved_problem_ids": solved_problem_ids,
        },
    )


def problem_detail(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    category = problem.category

    solved = False
    saved_code = ""
    if request.user.is_authenticated:
        sub = Submission.objects.filter(
            user=request.user, problem=problem
        ).first()
        if sub:
            solved = True
            if sub.code:
                saved_code = sub.code

    return render(
        request,
        "problems/problem_detail.html",
        context={
            "problem": problem,
            "category": category,
            "solved": solved,
            "saved_code": saved_code,
        },
    )


@login_required(login_url="/auth/login/")
def problem_submit(request, pk):

    problem = get_object_or_404(Problem, pk=pk)
    code = (request.POST.get("code") or "").strip()

    if not code:
        messages.warning(request, "Kod kiriting.")
        return redirect("problems:detail", pk=pk)

    from submissions.runner import run_tests

    test_results = run_tests(code, problem)
    is_run_only = "run" in request.POST  # Run tugmasi bosilgan — faqat natija, submit emas

    if is_run_only:
        if test_results and all(r["passed"] for r in test_results):
            messages.info(request, "Barcha testlar o'tdi. Yuborish uchun «Yuborish» tugmasini bosing.")
        elif test_results:
            messages.warning(request, "Ba'zi testlar o'tmadi. Kodni to'g'rilang.")
    else:
        # Yuborish tugmasi — natija + Submission
        if test_results and all(r["passed"] for r in test_results):
            Submission.objects.update_or_create(
                user=request.user,
                problem=problem,
                defaults={"code": code},
            )
            messages.success(request, "Yechimingiz qabul qilindi. Yechildi!")
        elif test_results:
            messages.warning(request, "Ba'zi testlar o'tmadi. Barcha testlar o'tguncha yuborilmaydi.")

    solved = Submission.objects.filter(
        user=request.user, problem=problem
    ).exists()
    category = problem.category

    return render(
        request,
        "problems/problem_detail.html",
        context={
            "problem": problem,
            "category": category,
            "solved": solved,
            "test_results": test_results,
            "submitted_code": code,
        },
    )
