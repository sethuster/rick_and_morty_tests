"""
Test module for API requests using pytest and requests.

This module provides example tests for HTTP requests to external APIs.
"""

import pytest, requests, json, os
from jsonschema import validate, ValidationError
from .conftest import rick_api_base_url
import schemas

class TestCharacterAPI:
    BASE_URL = rick_api_base_url()
    ALL_CHARACTERS = []

    @pytest.fixture(scope="session")
    def get_all_characters(self):
        return requests.get(f"{self.BASE_URL}/character")

    def test_get_all_chars_preamble(self, get_all_characters):
        """
        Validate the preamble is as expected
        Info section contains, count, pages, prev and next
        """
        assert get_all_characters.status_code == 200
        assert "results" in get_all_characters.json()
        assert "info" in get_all_characters.json()

    def test_get_all_characters_paginated(self, get_all_characters):
        """
        Validate that the character results are paginated
        """
        info = get_all_characters.json()["info"]
        assert "count" in info
        assert "pages" in info
        assert info["pages"] >= 0
        assert "prev" in info
        assert "next" in info

    
    def test_get_all_characters_paginated(self, get_all_characters):
        """
        Validate that the characters are paginated
        each page of results should contain different characters
        """
        resp = get_all_characters
        while resp.json()["info"]["next"] is not None:
            print(f"Evalutating {resp.json()["info"]["next"]}")
            next_resp = requests.get(resp.json()["info"]["next"])
            for char in next_resp.json()["results"]:
                assert char not in resp.json()["results"], f"Found duplicate value for '{char['name']}' on multiple pages!"
            for char in resp.json()["results"]:
                self.ALL_CHARACTERS.append(char)
            resp = next_resp
        for char in resp.json()["results"]:
            self.ALL_CHARACTERS.append(char) # always append the last results to the list

        print(f"Local Chars {len(self.ALL_CHARACTERS)} - API Count {resp.json()["info"]["count"]}")
        if len(self.ALL_CHARACTERS) == resp.json()["info"]["count"]:
            print("writing results to a file for later")
            file_path = os.path.join(os.path.dirname(__file__), "all_characters.json")
            with open(file_path, "w") as f:
                json.dump(self.ALL_CHARACTERS, f, indent=2)



# class TestAPIRequests:
#     """Test class for API request operations."""
    
#     BASE_URL = "https://rickandmortyapi.com/api"
    
#     def test_get_all_characters(self):
#         """Test fetching all characters from the API."""
#         response = requests.get(f"{self.BASE_URL}/character")
        
#         assert response.status_code == 200
#         assert "results" in response.json()
#         assert "info" in response.json()
        
#         data = response.json()
#         assert isinstance(data["results"], list)
#         assert len(data["results"]) > 0
    
#     def test_get_character_by_id(self):
#         """Test fetching a specific character by ID."""
#         character_id = 1
#         response = requests.get(f"{self.BASE_URL}/character/{character_id}")
        
#         assert response.status_code == 200
#         data = response.json()
        
#         assert data["id"] == character_id
#         assert "name" in data
#         assert "status" in data
#         assert "species" in data
    
#     def test_get_characters_with_query_params(self):
#         """Test fetching characters with query parameters."""
#         params = {"name": "Rick Sanchez"}
#         response = requests.get(f"{self.BASE_URL}/character", params=params)
        
#         assert response.status_code == 200
#         data = response.json()
#         assert len(data["results"]) > 0
#         assert data["results"][0]["name"] == "Rick Sanchez"
    
#     def test_invalid_character_id_returns_404(self):
#         """Test that an invalid character ID returns 404."""
#         invalid_id = 999999
#         response = requests.get(f"{self.BASE_URL}/character/{invalid_id}")
        
#         assert response.status_code == 404
    
#     def test_timeout_handling(self):
#         """Test request timeout handling."""
#         with pytest.raises(requests.exceptions.Timeout):
#             requests.get(f"{self.BASE_URL}/character", timeout=0.0001)


# @pytest.fixture
# def sample_character_id() -> int:
#     """Fixture providing a sample character ID."""
#     return 1


# @pytest.fixture
# def api_base_url() -> str:
#     """Fixture providing the base API URL."""
#     return "https://rickandmortyapi.com/api"


# @pytest.mark.parametrize("endpoint,expected_keys", [
#     ("character", ["info", "results"]),
#     ("location", ["info", "results"]),
#     ("episode", ["info", "results"]),
# ])
# def test_api_endpoints_have_expected_structure(endpoint, expected_keys):
#     """Parametrized test for different API endpoints."""
#     base_url = "https://rickandmortyapi.com/api"
#     response = requests.get(f"{base_url}/{endpoint}")
    
#     assert response.status_code == 200
#     data = response.json()
    
#     for key in expected_keys:
#         assert key in data

