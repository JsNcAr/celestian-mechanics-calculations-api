"""Tests for math helper utilities."""

import math

from app.utils.math_helpers import (
    deg_to_rad,
    normalize_angle_deg,
    normalize_angle_rad,
    rad_to_deg,
)


def test_deg_to_rad() -> None:
    assert math.isclose(deg_to_rad(180.0), math.pi)
    assert math.isclose(deg_to_rad(90.0), math.pi / 2)


def test_rad_to_deg() -> None:
    assert math.isclose(rad_to_deg(math.pi), 180.0)
    assert math.isclose(rad_to_deg(math.pi / 2), 90.0)


def test_normalize_angle_deg() -> None:
    assert math.isclose(normalize_angle_deg(360.0), 0.0)
    assert math.isclose(normalize_angle_deg(450.0), 90.0)
    assert math.isclose(normalize_angle_deg(-90.0), 270.0)


def test_normalize_angle_rad() -> None:
    assert math.isclose(normalize_angle_rad(2 * math.pi), 0.0)
    assert math.isclose(normalize_angle_rad(3 * math.pi), math.pi)
