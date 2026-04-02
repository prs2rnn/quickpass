import pytest
from unittest.mock import patch
import string
import sys
from io import StringIO
import argparse

from src.quickpass import (
    build_character_set,
    validate_password_generation,
    generate_password,
    parse_args,
    main
)


class TestPasswordGenerator:

    def test_build_character_set_all_enabled(self):
        """Test: all character types are enabled"""
        result = build_character_set(True, True, True, True)
        expected = string.digits + string.ascii_uppercase + string.ascii_lowercase + string.punctuation
        assert set(result) == set(expected)

    def test_build_character_set_only_digits(self):
        """Test: only digits are enabled"""
        result = build_character_set(True, False, False, False)
        assert result == string.digits

    def test_build_character_set_no_types(self):
        """Test: no character types are enabled"""
        result = build_character_set(False, False, False, False)
        assert result == ''

    def test_validate_password_generation_valid(self):
        """Test: validation passes for valid parameters"""
        char_set = 'abc123'
        validate_password_generation(10, char_set)  # Should not raise any exception

    def test_validate_password_generation_zero_length(self):
        """Test: error when length is zero"""
        with pytest.raises(ValueError) as exc_info:
            validate_password_generation(0, 'abc')
        assert 'Length must be a positive integer (> 0)' in str(exc_info.value)

    def test_validate_password_generation_negative_length(self):
        """Test: error when length is negative"""
        with pytest.raises(ValueError) as exc_info:
            validate_password_generation(-5, 'abc')
        assert 'Length must be a positive integer (> 0)' in str(exc_info.value)

    def test_validate_password_generation_empty_char_set(self):
        """Test: error when character set is empty"""
        with pytest.raises(ValueError) as exc_info:
            validate_password_generation(10, '')
        assert 'Must be at least 1 type of symbols enabled' in str(exc_info.value)

    def test_generate_password_correct_length(self):
        """Test: password has correct length"""
        password = generate_password(15, True, True, True, True)
        assert len(password) == 15

    @pytest.mark.parametrize("length", [1, 5, 20, 50])
    def test_generate_password_various_lengths(self, length):
        """Test: passwords of various lengths are generated correctly"""
        password = generate_password(length, True, True, True, True)
        assert len(password) == length

    def test_generate_password_contains_required_chars_digits_only(self):
        """Test: password contains only digits when only digits are enabled"""
        password = generate_password(10, True, False, False, False)
        assert all(c in string.digits for c in password)

    def test_generate_password_contains_required_chars_uppercase_only(self):
        """Test: password contains only uppercase letters when only uppercase is enabled"""
        password = generate_password(10, False, True, False, False)
        assert all(c in string.ascii_uppercase for c in password)

    def test_generate_password_contains_required_chars_lowercase_only(self):
        """Test: password contains only lowercase letters when only lowercase is enabled"""
        password = generate_password(10, False, False, True, False)
        assert all(c in string.ascii_lowercase for c in password)

    def test_generate_password_contains_required_chars_special_only(self):
        """Test: password contains only special characters when only special is enabled"""
        password = generate_password(10, False, False, False, True)
        assert all(c in string.punctuation for c in password)

    def test_generate_password_empty_char_set_raises_error(self):
        """Test: exception is raised when character set is empty"""
        with pytest.raises(ValueError):
            generate_password(10, False, False, False, False)

    @patch('argparse.ArgumentParser.parse_args')
    def test_parse_args_default_values(self, mock_parse_args):
        """Test: default values are correctly set"""
        mock_parse_args.return_value = argparse.Namespace(
            length=20, use_digits=True, use_upper=True,
            use_lower=True, use_special=True, count=1
        )
        args = parse_args()
        assert args.length == 20
        assert args.count == 1
        assert args.use_digits is True

    @patch('argparse.ArgumentParser.parse_args')
    def test_parse_args_custom_values(self, mock_parse_args):
        """Test: custom values are correctly parsed"""
        mock_parse_args.return_value = argparse.Namespace(
            length=15, use_digits=False, use_upper=False,
            use_lower=True, use_special=False, count=3
        )
        args = parse_args()
        assert args.length == 15
        assert args.use_digits is False
        assert args.count == 3
