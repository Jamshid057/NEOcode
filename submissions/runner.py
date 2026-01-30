"""
Foydalanuvchi kodini test case'lar bo'yicha ishga tushirish va natijani solishtirish.
Input: vergul bilan ajratilgan (masalan "10, 20").
"""


def _parse_input(input_str):
    """Vergul bilan ajratilgan qatorni argumentlar ro'yxatiga aylantiradi."""
    if not (input_str or input_str.strip()):
        return []
    parts = [p.strip() for p in input_str.strip().split(",")]
    result = []
    for p in parts:
        try:
            result.append(int(p))
        except ValueError:
            try:
                result.append(float(p))
            except ValueError:
                result.append(p)
    return result


def _normalize_output(value):
    """Natijani solishtirish uchun bitta ko'rinishga keltiradi."""
    if value is None:
        return "None"
    s = str(value).strip()
    return s


def run_tests(code: str, problem) -> list[dict]:
    """
    Foydalanuvchi kodini barcha test case'lar bo'yicha ishga tushiradi.
    Har bir test uchun: input_data, expected_output, actual_output, passed (True/False).
    """
    from problems.models import TestCase

    test_cases = problem.test_cases.all().order_by("order", "pk")
    if not test_cases.exists():
        return []

    # Foydalanuvchi kodini bajarib funksiyani olamiz
    namespace = {}
    try:
        exec(code, namespace)
    except SyntaxError as e:
        return [
            {
                "input_data": tc.input_data,
                "expected_output": tc.expected_output,
                "actual_output": f"SyntaxError: {e}",
                "passed": False,
            }
            for tc in test_cases
        ]
    except Exception as e:
        return [
            {
                "input_data": tc.input_data,
                "expected_output": tc.expected_output,
                "actual_output": f"Xato: {type(e).__name__}: {e}",
                "passed": False,
            }
            for tc in test_cases
        ]

    func = namespace.get(problem.function_name)
    if not callable(func):
        return [
            {
                "input_data": tc.input_data,
                "expected_output": tc.expected_output,
                "actual_output": f"Funksiya topilmadi: {problem.function_name}",
                "passed": False,
            }
            for tc in test_cases
        ]

    results = []
    for tc in test_cases:
        try:
            args = _parse_input(tc.input_data)
            result = func(*args)
            actual = _normalize_output(result)
            expected = _normalize_output(tc.expected_output)
            passed = actual == expected
            results.append(
                {
                    "input_data": tc.input_data,
                    "expected_output": tc.expected_output,
                    "actual_output": actual,
                    "passed": passed,
                }
            )
        except Exception as e:
            results.append(
                {
                    "input_data": tc.input_data,
                    "expected_output": tc.expected_output,
                    "actual_output": f"Xato: {type(e).__name__}: {e}",
                    "passed": False,
                }
            )
    return results
