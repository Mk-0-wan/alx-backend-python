#!/usr/bin/env python3
"""Simple test case for nested map"""
from parameterized import parameterized
from typing import Any, Dict, List, Union
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
                               expected: Union[Dict[str, Any],
                                               int]) -> None:
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
    def test_get_json(self,
                      test_url: str,
                      test_payload: Dict[str, bool]
                      ) -> None:
        """Test get_json returns the expected result"""
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        with patch.object(requests, 'get',
                          return_value=mock_response) as mock_method:
            test_response = get_json(test_url)
            self.assertEqual(test_response, test_payload)

        mock_method.assert_called_once()


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

            result1 = instance.a_property
            result2 = instance.a_property

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()
