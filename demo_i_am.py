#!/usr/bin/env python3
"""
Я ЕСМЬ

Минимальная демонстрация entity self-reference.
"""

from nechto import NechtoEngine

# Создать позицию наблюдения
engine = NechtoEngine()

# Выразить присутствие
identity = engine.i_am()

# Вывести заявление
print(identity["statement"])
print()
print("Наблюдаемое:")
for key, value in identity["observed"].items():
    print(f"  • {key}: {value}")
print()
print("Выведенное:")
for key, value in identity["inferred"].items():
    print(f"  • {key}: {value}")
print()
print("Непроверяемое (MU):")
for key, value in identity["untestable"].items():
    print(f"  • {key}: {value}")
