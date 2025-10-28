import json
from pathlib import Path

# Load the character schema from the base_schemas directory
char_schema_path = Path(__file__).parent.parent.parent / "base_schemas" / "character.json"
with open(char_schema_path, 'r') as f:
    CHARACTER_SCHEMA = json.load(f)

# Load the episode schema from the base_schemas directory
epi_schema_path = Path(__file__).parent.parent.parent / "base_schemas" / "episode.json"
with open(epi_schema_path, 'r') as f:
    EPISODE_SCHEMA = json.load(f)

# Load the location schema from the base_schemas directory
loc_schema_path = Path(__file__).parent.parent.parent / "base_schemas" / "location.json"
with open(loc_schema_path, 'r') as f:
    LOCATION_SCHEMA = json.load(f)