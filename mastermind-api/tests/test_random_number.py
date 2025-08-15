"""
    Tests for secret number generation, function found in the random_number.py file.
    Cover both external API functionality and local fallback.
"""

import pytest
from unittest.mock import patch, Mock
import requests
from app.client.random_number import get_secret_number

class TestGetSecretNumber:
    """
        Tests for the get_secret_number function.
    """

    def test_difficulty_level_1_configuration(self):
        """
            Test the correct configuration for difficulty level 1
        """
        with patch('app.client.random_number.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.text = "1 2 3 4"
            mock_response.raise_for_status.return_value = None
            mock_get.return_value =  mock_response

            number, attempts = get_secret_number(1)

            # Verify correct configuration for difficulty level 1
            assert len(number) == 4
            assert attempts == 12

            # Verify that the API was called with correct parameters
            mock_get.assert_called_once()
            call_args = mock_get.call_args[0][0]
            assert "max=5" in call_args # For difficulty level 1 max_digit must be 5

    def test_difficulty_level_2_configuration(self):
        """
            Test the correct configuration for difficulty level 2
        """

        with patch('app.client.random_number.requests.get') as mock_get:
            
            mock_response = Mock()
            mock_response.text = "3 5 7 1"
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            number, attempts = get_secret_number(2)

            assert len(number) == 4
            assert attempts == 10

            #Verify that the API was called with correct parameters
            call_args = mock_get.call_args[0][0]
            assert "max=7" in call_args # For difficulty level 2 max_digit must be 7

    
    def test_difficulty_level_3_configuration(self):
        """
            Test the correct configuration for difficult level 3
        """

        with patch('app.client.random_number.requests.get') as mock_get:

            mock_response = Mock()
            mock_response.text = "9 4 2 3"
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            number, attempts = get_secret_number(3)

            assert len(number) == 4
            assert attempts == 8

            call_args= mock_get.call_args[0][0]
            assert "max=9" in call_args # For difficulty level 3 max_digit must be 9 


    def test_successfull_api_call(self):
        """
            Test successfull call to random.org API.
        """

        with patch('app.client.random_number.requests.get') as mock_get:


            mock_response = Mock()
            mock_response.text = "4 5 2 3"
            mock_response.raise_for_status.return_value= None
            mock_get.return_value = mock_response

            number, attempts = get_secret_number(1)

            assert number == ['4','5','2','3']
            assert attempts == 12

            mock_get.assert_called_once()
            assert mock_response.raise_for_status.called

    def test_api_request_exception_fallback(self):
        """
            Test for fallback to local generation  when API fails
        """
        with patch('app.client.random_number.requests.get') as mock_get, \
            patch('app.client.random_number.random.randint') as mock_randint:

            # Simulate API failure
            mock_get.side_effect = requests.RequestException("API unavailable")
            
            # Simulate specific local random numbers
            mock_randint.side_effect = [1,2,3,4]
            
            
            number, attempts = get_secret_number(1)

            # Must use local fallback 
            assert number == ['1','2','3','4']
            assert attempts == 12
            
            # Verify that an attempt was made to generate the secret number with the API and failed
            mock_get.assert_called_once()

            # Verify the local random was used
            assert mock_randint.call_count == 4

            # Verify that the correct parameters were called (0, 5 for difficulty 1)
            for call in mock_randint.call_args_list:
                assert call[0] == (0, 5)


    def test_api_http_error_fallback(self):
        """
            Test fallback when API return HTTP error
        """

        with patch('app.client.random_number.requests.get') as mock_get, \
            patch('app.client.random_number.random.randint') as mock_randint:

            #Simulate 500 HTTP error
            mock_response = Mock()
            mock_response.raise_for_status.side_effect = requests.HTTPError("500 Server Error")
            mock_get.return_value = mock_response

            mock_randint.side_effect = [7, 6, 5, 4]

            number,attempts = get_secret_number(2)

            # Must use fallback
            assert number == ['7', '6', '5', '4']
            assert attempts == 10

            # Verify that random.radint was called with correct max_digit for difficulty level 2
            for call in mock_randint.call_args_list:
                assert call[0] == (0,7)