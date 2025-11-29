"""
Test module for API requests using pytest and requests.

This module provides example tests for HTTP requests to external APIs.
"""

from unittest import skip
import pytest, requests, json, os
from jsonschema import validate, ValidationError
from .conftest import rick_api_base_url
import schemas, os, random, time
from pathlib import Path

class TestCharacterAPI:
    BASE_URL = rick_api_base_url()

    # WE want to load a local copy of the characters if it exists so we don't DDOS RAM API
    # mainly for local development of the tests
    all_chars_file = Path(__file__).parent / "all_characters.json"
    if os.path.exists(all_chars_file):
        with open(all_chars_file, 'r') as f:
            ALL_CHARACTERS = json.load(f)
    else:
        ALL_CHARACTERS = []

    def get_all_results(self, response):
        next = response.json()['info']['next']
        all_pages = response.json()['results']
        if next:
            while next is not None:
                resp = requests.get(next)
                all_pages.extend(resp.json()['results'])
                next = resp.json()['info']['next']
        return all_pages


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
        if len(self.ALL_CHARACTERS) > 0:
            self.ALL_CHARACTERS = []

        resp = get_all_characters
        while resp.json()["info"]["next"] is not None:
            print(f"Evalutating {resp.json()["info"]["next"]}")
            next_resp = requests.get(resp.json()["info"]["next"])
            if next_resp.json()["info"]["next"]:
                next_page = next_resp.json()["info"]["next"].split("page=")[1]
            for char in next_resp.json()["results"]:
                assert char not in resp.json()["results"], f"Found duplicate value for '{char['name']}' on page {next_page-1} and {next_page}!"
            for char in resp.json()["results"]:
                self.ALL_CHARACTERS.append(char)
            resp = next_resp
        for char in resp.json()["results"]:
            self.ALL_CHARACTERS.append(char) # always append the last results to the list

        print(f"Retrieved Chars {len(self.ALL_CHARACTERS)} vs API Count {resp.json()["info"]["count"]}")
        if len(self.ALL_CHARACTERS) == resp.json()["info"]["count"]:
            print("writing results to a file for later")
            file_path = os.path.join(os.path.dirname(__file__), "all_characters.json")
            with open(file_path, "w") as f:
                json.dump(self.ALL_CHARACTERS, f, indent=2)

    
    def test_get_single_character(self, get_all_characters):
        """
        Validate that the API will return a single character properly

        At this point in the test cycle we should have a list of all the characters in memory
        select a random character of that list to retrieve
        """

        char = random.choice(self.ALL_CHARACTERS)
        resp = requests.get(f"{self.BASE_URL}/character/{char['id']}")
        assert resp.status_code == 200, f"Status code incorrect.  Unable to retrieve {char['name']} by id: {char['id']}"
        assert resp.json() == char, f"Returned character isn't as expected."
        try: 
            validate(resp.json(), schemas.CHARACTER_SCHEMA)
        except ValidationError as e:
            pytest.fail(f"Character schema for character:id[{char['id']}] did not match expected schema.")


    def test_get_multiple_characters_csv(self, get_all_characters):
        """
        Validate that the API will return multiple charaters using the csv method provided by the API

        1. Validate the API returns between 3 and 5 selected characters

        At this point in the test cycle we should have a list of all the characters in memory
        select a random character of that list to retrieve
        """
        num_chars = random.randint(3, 5)
        chars = []
        chars_s = ''
        for char in range(num_chars):
            choice = random.choice(self.ALL_CHARACTERS)
            chars.append(choice)
            chars_s += f"{choice['id']},"
        chars_s = chars_s.rstrip(',')
        resp = requests.get(f"{self.BASE_URL}/character/{chars_s}")
        assert resp.status_code == 200, f"Retrieving multiple characters via CSV failed! {resp.text}"
        for char in chars:
            assert char in resp.json()

    def test_get_multiple_characters_array(self, get_all_characters):
        """
        Validate that the API will return multiple characters using the array method provided by the API

        
        1. Validate the API returns between 3 and 5 selected characters

        At this point in the test cycle we should have a list of all the characters in memory
        select a random character of that list to retrieve
        """
        num_chars = random.randint(3, 5)
        chars = []
        for char in range(num_chars):
            choice = random.choice(self.ALL_CHARACTERS)
            chars.append(choice)
        ids = [c['id'] for c in chars]
        url = f"{self.BASE_URL}/character/{ids}"
        resp = requests.get(url)
        assert resp.status_code == 200, f"Retrieving mulitiple characters via ARRAY failed: {resp.text}"
        for char in chars:
            assert char in resp.json(), f"Expected {char['id']} in response!"
            
    def test_get_characters_by_filter_name(self, get_all_characters):
        """
        Validate that the name filter works as expected.  Providing a name to the API should return all characters
        with a name that matches
        """
        rand_char = random.choice(self.ALL_CHARACTERS)
        resp = requests.get(f"{self.BASE_URL}/character/?name={rand_char['name']}")
        assert resp.status_code == 200, f"There was something wrong with the name filter: {resp.text}"
        all_matches = self.get_all_results(resp)
        if rand_char not in all_matches:
            pytest.fail(f"name: {rand_char['name']} id: {rand_char['id']} not returned as expected!")

    def test_get_characters_by_filter_status(self, get_all_characters):
        """
        Validate that the characters can be filtered by status
        """
        rand_char = random.choice(self.ALL_CHARACTERS)
        resp = requests.get(f"{self.BASE_URL}/character/?status={rand_char['status']}")
        assert resp.status_code == 200, f"There was something wrong with the status filter: {resp.text}"
        all_matches = self.get_all_results(resp)
        print(f"Found {len(all_matches)} characters with status of {rand_char['status']}")
        if rand_char not in all_matches:
            pytest.fail(f"{rand_char['name']} {rand_char['id']} {rand_char['status']} was not found in results!")

    def test_get_characters_by_filter_species(self, get_all_characters):
        """
        Validate that the characters can be filtered by species
        """
        rand_char = random.choice(self.ALL_CHARACTERS)
        resp = requests.get(f"{self.BASE_URL}/character/?species={rand_char['species']}")
        assert resp.status_code == 200, f"There was something wrong with the species filter: {resp.text}"
        all_matches = self.get_all_results(resp)
        print(f"Found {len(all_matches)} characters with species of {rand_char['species']}")
        if rand_char not in all_matches:
            pytest.fail(f"{rand_char['name']} {rand_char['id']} {rand_char['species']} was not found in results!")

    def test_get_characters_by_filter_type(self, get_all_characters):
        """
        Validate that the characters can be filtered by type
        """
        rand_char = random.choice(self.ALL_CHARACTERS)
        resp = requests.get(f"{self.BASE_URL}/character/?type={rand_char['type']}")
        assert resp.status_code == 200, f"There was something wrong with the type filter: {resp.text}"
        all_matches = self.get_all_results(resp)
        print(f"Found {len(all_matches)} characters with type of {rand_char['type']}")
        if rand_char not in all_matches:
            pytest.fail(f"{rand_char['name']} {rand_char['id']} {rand_char['type']} was not found in results!")

    def test_get_characters_by_filter_gender(self, get_all_characters):
        """
        Validate that the characters can be filtered by gender
        """
        rand_char = random.choice(self.ALL_CHARACTERS)
        resp = requests.get(f"{self.BASE_URL}/character/?gender={rand_char['gender']}")
        assert resp.status_code == 200, f"There was something wrong with the gender filter: {resp.text}"
        all_matches = self.get_all_results(resp)
        print(f"Found {len(all_matches)} characters with gender of {rand_char['gender']}")
        if rand_char not in all_matches:
            pytest.fail(f"{rand_char['name']} {rand_char['id']} {rand_char['gender']} was not found in results!")
    

        

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

