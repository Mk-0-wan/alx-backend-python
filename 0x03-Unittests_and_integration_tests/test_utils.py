#!/usr/bin/env python3
"""Simple test case for nested map"""
from parameterized import parameterized
from typing import Any, Dict, List
import unittest
from unittest.mock import Mock, patch
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test Case for access nested map"""
    @parameterized.expand([
       ({"a": 1}, ("a",), 1),
       ({"a": {"b": 2}}, ("a",), {"b": 2}),
       ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self,
                               nested_map: Dict[str, Any],
                               path: List[str],
                               expected: Any) -> None:
        """test case for the access nested map func"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError)
        ])
    def test_access_nested_map_exception(self,
                                         nested_map: Dict[str, Any],
                                         path: List[str],
                                         err: Any) -> None:
        """Handling all the key errors passed"""
        with self.assertRaises(err):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Testing the get_json method"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('requests.get')
    def test_get_json(self,
                      test_url: str,
                      test_payload: Dict[str, bool],
                      mock_get: object) -> None:
        """Test get_json returns the expected result"""
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        # Call get_json with test_url and assert the result
        result = get_json(test_url)
        self.assertEqual(result, test_payload)

        # Assert that requests.get was called once with the test_url
        mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """test case for memoization method"""
    def test_memoize(self) -> None:
        """method to test for the memoize wrapper method"""
        class TestClass:
            "class test for the memoize func"
            def a_method(self) -> int:
                """forgot to document"""
                return 42

            @memoize
            def a_property(self) -> int:
                "tester for the memoize func"
                return self.a_method()

        with patch.object(
                TestClass,
                'a_method',
                return_value=42
                ) as mock_method:
            instance = TestClass()

            # Call a_property twice
            result1 = instance.a_property
            result2 = instance.a_property

            # Check that a_method was called only once
            mock_method.assert_called_once()

            # Check that the results are correct
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
