# Automatically generated by Pynguin.
import triangle as module_0


def test_case_0():
    int_0 = 1516
    str_0 = module_0.triangle(int_0, int_0, int_0)
    assert str_0 == 'Equilateral triangle'


def test_case_1():
    int_0 = 1879
    int_1 = -5272
    str_0 = module_0.triangle(int_0, int_1, int_1)
    assert str_0 == 'Isosceles triangle'


def test_case_2():
    int_0 = -2102
    int_1 = -1289
    int_2 = 1167
    str_0 = module_0.triangle(int_0, int_1, int_2)
    assert str_0 == 'Scalene triangle'
    str_1 = module_0.triangle(int_0, int_0, int_1)
    assert str_1 == 'Isosceles triangle'


def test_case_3():
    int_0 = -4086
    int_1 = 518
    str_0 = module_0.triangle(int_1, int_1, int_1)
    assert str_0 == 'Equilateral triangle'
    int_2 = -3861
    str_1 = module_0.triangle(int_0, int_0, int_2)
    assert str_1 == 'Isosceles triangle'
    int_3 = -368
    int_4 = -192
    str_2 = module_0.triangle(int_3, int_4, int_3)
    assert str_2 == 'Isosceles triangle'

count_passed_test_cases = 0
try:
	test_case_0()
	count_passed_test_cases += 1
except Exception:
	pass
try:
	test_case_1()
	count_passed_test_cases += 1
except Exception:
	pass
try:
	test_case_2()
	count_passed_test_cases += 1
except Exception:
	pass
try:
	test_case_3()
	count_passed_test_cases += 1
except Exception:
	pass
print(count_passed_test_cases)