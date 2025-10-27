# Rick and Morty API tests

The idea of this repo is to add a bunch of rick and morty api (and UI) tests with different languages and frameworks. Practice making the best tests in each language and each type.  Research and compare different testing libraries and techniques.

## The Tests

Tests for each language will be broken up into different directories.  Each directory will have and API test directory and a UI test directory.  Each directory will have a Makefile with standard commands that will get each test suite going for that language.

### Makefile Commands

`make build`: setup the dirctory with the language and packages needed to run the tests
`make test-api`: run the API tests for that language and test framework
`make test-ui`: run the UI tests for that language and test framework

### API Tests for each language

Each language will have the following API Tests:

#### Character
| Test | Assertions | Endpoint | Notes |
| ---- | ------- | ----- | ----| 
| char_schema | Validate that the character schema is consistent | NA | See character schema for more information |
| get_all_chars_paginated | Results are paginated and not all characters are returned in one go | `api/character` | |
| get_all_chars_preamble | Preamble for characters list is accurate with count, page, next and prev pages |  `api/character` | The premble is the data above the results list |
| get_all_chars_pages | validate that the characters are different on each page and no repeated data exists |  `api/character` | |
| get_single_character | A single character can be retireved properly | `api/character/[id]` | Characters can be retrieved by ID appropriately | 
| get_multiple_characters_csv | multple characters can be rerieved from the API | `api/character/[id],[id],[id]` | how many characters can be retireved at once? |
| get_multiple_characters_array | multple characters can be rerieved from the API | `api/character/[[id],[id],[id]]` | how many characters can be retireved at once? |
| get_characters_by_filter_name | characters can be returned by matching certain criteria | `api/character/?name=rick` | Filters are passed as url params |
| get_characters_by_filter_status | characters can be returned by matching certain criteria | `api/character/?status=alive` | |
| get_characters_by_filter_species | characters can be returned by matching certain criteria | `api/character/?species=human` | |
| get_characters_by_filter_type | characters can be returned by matching certain criteria | `api/character/?type=robot` | need to find a good example of type |
| get_characters_by_filter_gender | characters can be returned by matching certain criteria | `api/character/?gender=genderless` | |
| get_characters_by_filter_invalid_param | filtering by an invalid status provides a friendly error message | `api/character/?invalid=true` | The should provide a friendly error|
| get_invalid_character | Make sure the API handles looking for invalid characters | `api/character/[invalidID]` | API should return proper, user friendly error and code |
| get_multiple_characters_invalid_csv | API handles retrieving characters with invalid values | `api/character/[invID],[id],[id]` | |
| get_multiple_characters_invalid_csv_spacing | API handles retrieving characters with invalid values | `api/character/[invID], [id], [id]` | |
| get_multiple_characters_csv_max | API can a large list of specific characters | `api/character/[invID],[id],[id]` | Find the max characters the API can handle |
| get_multiple_characters_invalid_array | The API should handle retrieving an invalid character ID in the array | `api/character/[[id],[invId],[id]]` |  |
| get_multiple_characters_invalid_array_spacing | API handles retrieving characters with invalid values | `api/character/[[ID], [id], [id]]` | |
| get_multiple_characters_invalid_array_max | API can handle a large list of specific characters or provides friendly max error | `api/character/[invID], [id], [id]` | |


##### Character filters lis
| param | type | values | 
| ----- | ---- | ------ |
| name | string | any character name | 
| status | selection | alive, dead, unknown | 
| species | string | human, birdperson, etc |
| type | string | not sure what this would be |
| gender | selection | female, male, genderless, unknown |
