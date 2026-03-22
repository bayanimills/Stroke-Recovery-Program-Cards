"""Tests for the SRP Cards CLI exercise sheet generator."""

import os
import tempfile

import pytest

from cli.exercise_sheet import EXERCISES, generate_sheet, parse_position


class TestExerciseDatabase:
    def test_all_categories_present(self):
        assert set(EXERCISES.keys()) == {"hand", "shoulder", "arm", "leg"}

    def test_each_category_has_exercises(self):
        for category, data in EXERCISES.items():
            assert len(data["exercises"]) >= 1, f"{category} has no exercises"

    def test_each_category_has_required_fields(self):
        for category, data in EXERCISES.items():
            assert "hex" in data, f"{category} missing hex"
            assert "shape" in data, f"{category} missing shape"
            assert "num" in data, f"{category} missing num"
            assert "title" in data, f"{category} missing title"

    def test_exercises_have_steps(self):
        for category, data in EXERCISES.items():
            for ex in data["exercises"]:
                assert "name" in ex
                assert "steps" in ex
                assert len(ex["steps"]) >= 1


class TestParsePosition:
    def test_valid_positions(self):
        assert parse_position("hand_0") == ("hand", 0)
        assert parse_position("shoulder_2") == ("shoulder", 2)
        assert parse_position("arm_1") == ("arm", 1)
        assert parse_position("leg_0") == ("leg", 0)

    def test_invalid_format_no_underscore(self):
        with pytest.raises(ValueError, match="Invalid position format"):
            parse_position("hand0")

    def test_invalid_format_bad_index(self):
        with pytest.raises(ValueError, match="Index must be a number"):
            parse_position("hand_abc")

    def test_unknown_exercise_type(self):
        with pytest.raises(ValueError, match="Unknown exercise type"):
            parse_position("foot_0")


class TestGenerateSheet:
    def test_four_layout_creates_pdf(self):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            output = f.name
        try:
            generate_sheet(
                output,
                ("hand", 0),
                ("shoulder", 1),
                ("arm", 2),
                ("leg", 0),
                layout="four",
            )
            assert os.path.exists(output)
            assert os.path.getsize(output) > 0
        finally:
            os.unlink(output)

    def test_single_layout_creates_pdf(self):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            output = f.name
        try:
            generate_sheet(
                output,
                ("hand", 0),
                ("shoulder", 0),
                ("arm", 0),
                ("leg", 0),
                layout="single",
            )
            assert os.path.exists(output)
            assert os.path.getsize(output) > 0
        finally:
            os.unlink(output)

    def test_all_exercise_combinations(self):
        """Verify every exercise can be rendered without error."""
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            output = f.name
        try:
            for cat in EXERCISES:
                for idx in range(len(EXERCISES[cat]["exercises"])):
                    generate_sheet(
                        output,
                        (cat, idx),
                        (cat, idx),
                        (cat, idx),
                        (cat, idx),
                    )
        finally:
            os.unlink(output)
