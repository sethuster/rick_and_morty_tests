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
| get_all_chars_preamble | Preamble for characters list is accurate with count, page, next and prev pages |  `api/character` | The premble is the data above the results list |
| get_all_chars_paginated | Results are paginated and not all characters are returned in one go | `api/character` | |
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

##### Character filters list
| param | type | values | 
| ----- | ---- | ------ |
| name | string | any character name | 
| status | selection | alive, dead, unknown | 
| species | string | human, birdperson, etc |
| type | string | not sure what this would be |
| gender | selection | female, male, genderless, unknown |


#### Location 
| Test | Assertions | Endpoint | Notes |
| ---- | ------- | ----- | ----| 
| location_schema | validate the location schema is consistent | NA | see the location schema for more information | 
| get_all_locations_paginated | results are paginated and not all locations are returned in one go | `api/location` | |
| get_all_locations_preamble | preamble for locations list is accurate with count, page, next and prev | `api/location` | The preambe is the data above the results list |
| get_all_locations_pages | validate that each page shows different locations | `api/location` | Ensure that each page contains different data |
| get_single_location | validate that a single location can be retrieved | `api/location/[id]` | |
| get_multiple_locations_csv | multiple locations can be retrieved from the API | `api/location/[id],[id],[id]` | locations also accept a CSV format and array format | 
| get_multiple_locations_array | multiplocations can be retrieved from the API | `api/location/[id,id,id]` | |
| get_location_filter_name | locations can be retrieved by name | `api/location?name="citidel of ricks"` | names of locations can be used for filtering |
| get_location_filter_type | locations can be filtered by type | `api/location?type="space station"` | |
| get_location_filter_dimension | locations can be filtered by dimension | `api/location?dimension=unknown` | |
| get_location_invalid | invalid location is not retrieved and a friendly error is shown | `api/location/[invalidID]` | |
| get_location_csv_max | get the maximum number of locations in one request | `api/location/[id],[id],[id]` | there's gotta be a max here |
| get_location_array_max | get the maximum number of locations in one request | `api/location/[id,id,id]` | |
| get_multiple_locations_invalid_array | The API should handle retrieving an invalid location ID in the array | `api/location/[[id],[invId],[id]]` |  |
| get_multiple_locations_invalid_array_spacing | API handles retrieving location with invalid values | `api/location/[[ID], [id], [id]]` | |
| get_multiple_locations_invalid_array_max | API can handle a large list of specific location or provides friendly max error | `api/location/[invID], [id], [id]` | |

##### Location filters list
| param | type | values |
| ----- | ---- | ------ |
| name | string | location name |
| type | string | location type |
| dimension | string | location dimension |

#### Episode 
| Test | Assertions | Endpoint | Notes |
| ---- | ------- | ----- | ----| 
| episode_schema | validate the episode schema is consistent | NA | see the episode schema for more information | 
| get_all_episodes_paginated | results are paginated and not all episodes are returned in one go | `api/episode` | |
| get_all_episodes_preamble | preamble for episodes list is accurate with count, page, next and prev | `api/episode` | The preambe is the data above the results list |
| get_all_episodes_pages | validate that each page shows different episodes | `api/episode` | Ensure that each page contains different data |
| get_single_episode | validate that a single episode can be retrieved | `api/episode/[id]` | |
| get_multiple_episodes_csv | multiple episodes can be retrieved from the API | `api/episode/[id],[id],[id]` | episodes also accept a CSV format and array format | 
| get_multiple_episodes_array | multipepisodes can be retrieved from the API | `api/episode/[id,id,id]` | |
| get_episode_filter_name | episodes can be retrieved by name | `api/episode?name="citidel of ricks"` | names of episodes can be used for filtering |
| get_episode_filter_episode | episodes can be filtered by type | `api/episode?type="space station"` | |
| get_episode_csv_max | get the maximum number of episodes in one request | `api/episode/[id],[id],[id]` | there's gotta be a max here |
| get_episode_array_max | get the maximum number of episodes in one request | `api/episode/[id,id,id]` | |
| get_multiple_episodes_invalid_array | The API should handle retrieving an invalid episode ID in the array | `api/episode/[[id],[invId],[id]]` |  |
| get_multiple_episodes_invalid_array_spacing | API handles retrieving episode with invalid values | `api/episode/[[ID], [id], [id]]` | |
| get_multiple_episodes_invalid_array_max | API can handle a large list of specific episode or provides friendly max error | `api/episode/[invID], [id], [id]` | |

##### episode filters list
| param | type | values |
| ----- | ---- | ------ |
| name | string | episode name |
| episode | string | episode code used for tv |
