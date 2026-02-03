# 📊 Data Format Specification

This document defines the structure and format for all data files in GuessMyPlace.

## Overview

All data is stored in JSON format with specific schemas. Data files are versioned through Git and validated before deployment.

## Directory Structure

```
data/
├── places/
│   ├── countries.json
│   ├── cities.json
│   ├── historic_places.json
│   └── combined.json (auto-generated)
├── questions/
│   └── question_bank.json
├── schema/
│   ├── place_schema.json
│   └── question_schema.json
└── scripts/
    ├── generate_data.py
    ├── validate_data.py
    ├── combine_data.py
    └── enhance_data.py
```

---

## Place Data Format

### Schema

```json
{
  "id": "string (required, unique, snake_case)",
  "name": "string (required)",
  "type": "string (required, enum: ['country', 'city', 'historic_place'])",
  "characteristics": {
    "key": "value (string | number | boolean)"
  },
  "metadata": {
    "added_date": "string (ISO 8601)",
    "last_updated": "string (ISO 8601)",
    "contributors": ["string"],
    "verified": "boolean",
    "image_url": "string (optional)",
    "description": "string (optional)"
  }
}
```

### Example: Country

```json
{
  "id": "france",
  "name": "France",
  "type": "country",
  "characteristics": {
    "continent": "europe",
    "region": "western_europe",
    "has_coastline": true,
    "is_island": false,
    "population_millions": 67,
    "area_km2": 551695,
    "capital": "paris",
    "official_language": "french",
    "eu_member": true,
    "g7_member": true,
    "un_security_council": true,
    "currency": "euro",
    "drives_on": "right",
    "has_nuclear_weapons": true,
    "climate": "temperate",
    "famous_for": ["wine", "cheese", "fashion", "art"]
  },
  "metadata": {
    "added_date": "2026-01-15T00:00:00Z",
    "last_updated": "2026-02-01T12:30:00Z",
    "contributors": ["user123"],
    "verified": true,
    "image_url": "https://example.com/france.jpg",
    "description": "Western European country known for culture, cuisine, and landmarks"
  }
}
```

### Example: City

```json
{
  "id": "tokyo",
  "name": "Tokyo",
  "type": "city",
  "characteristics": {
    "continent": "asia",
    "country": "japan",
    "region": "east_asia",
    "is_capital": true,
    "is_coastal": true,
    "population_millions": 14,
    "metro_population_millions": 37,
    "has_metro": true,
    "has_airport": true,
    "climate": "humid_subtropical",
    "founded_year": 1457,
    "hosted_olympics": true,
    "olympic_years": [1964, 2020],
    "has_skyscrapers": true,
    "famous_landmarks": ["tokyo_tower", "shibuya_crossing", "imperial_palace"],
    "known_for": ["technology", "anime", "cuisine", "fashion"]
  },
  "metadata": {
    "added_date": "2026-01-15T00:00:00Z",
    "last_updated": "2026-01-20T09:15:00Z",
    "contributors": ["user456"],
    "verified": true,
    "image_url": "https://example.com/tokyo.jpg",
    "description": "Japan's capital, known for blending tradition with cutting-edge technology"
  }
}
```

### Example: Historic Place

```json
{
  "id": "eiffel_tower",
  "name": "Eiffel Tower",
  "type": "historic_place",
  "characteristics": {
    "continent": "europe",
    "country": "france",
    "city": "paris",
    "is_unesco": false,
    "built_year": 1889,
    "age_category": "modern",
    "is_monument": true,
    "is_building": true,
    "is_religious": false,
    "is_ancient": false,
    "is_ruins": false,
    "has_observation_deck": true,
    "material": "iron",
    "architectural_style": "art_nouveau",
    "height_meters": 330,
    "purpose": "exhibition",
    "can_enter_inside": true,
    "is_tower": true,
    "iconic_landmark": true,
    "tourist_attraction": true,
    "entrance_fee": true
  },
  "metadata": {
    "added_date": "2026-01-15T00:00:00Z",
    "last_updated": "2026-01-25T14:20:00Z",
    "contributors": ["user789"],
    "verified": true,
    "image_url": "https://example.com/eiffel.jpg",
    "description": "Iconic iron lattice tower built for the 1889 World's Fair"
  }
}
```

---

## Characteristic Guidelines

### Common Characteristics (All Types)

| Characteristic | Type | Values | Description |
|---------------|------|--------|-------------|
| `continent` | string | africa, antarctica, asia, europe, north_america, oceania, south_america | Geographic continent |
| `country` | string | ISO 3166-1 alpha-2 code or full name | Country location |
| `region` | string | Free-form | Sub-continental region |
| `climate` | string | tropical, arid, temperate, continental, polar | Climate type |
| `population_millions` | number | 0-2000 | Population in millions |

### Country-Specific Characteristics

| Characteristic | Type | Values | Description |
|---------------|------|--------|-------------|
| `has_coastline` | boolean | true/false | Has ocean/sea coast |
| `is_island` | boolean | true/false | Island nation |
| `is_landlocked` | boolean | true/false | No ocean access |
| `capital` | string | City name | Capital city |
| `official_language` | string/array | Language(s) | Official language(s) |
| `eu_member` | boolean | true/false | European Union member |
| `un_member` | boolean | true/false | United Nations member |
| `currency` | string | Currency name | Official currency |
| `drives_on` | string | left/right | Driving side |

### City-Specific Characteristics

| Characteristic | Type | Values | Description |
|---------------|------|--------|-------------|
| `is_capital` | boolean | true/false | National capital |
| `is_coastal` | boolean | true/false | On ocean/sea/large lake |
| `has_metro` | boolean | true/false | Has metro/subway system |
| `has_airport` | boolean | true/false | Has major airport |
| `metro_population_millions` | number | 0-40 | Metropolitan area population |
| `founded_year` | number | -3000 to present | Year founded |
| `hosted_olympics` | boolean | true/false | Hosted Olympic Games |

### Historic Place-Specific Characteristics

| Characteristic | Type | Values | Description |
|---------------|------|--------|-------------|
| `is_unesco` | boolean | true/false | UNESCO World Heritage Site |
| `built_year` | number | -3000 to present | Year constructed |
| `age_category` | string | ancient, medieval, modern, contemporary | Age classification |
| `is_monument` | boolean | true/false | Monument/memorial |
| `is_building` | boolean | true/false | Building structure |
| `is_religious` | boolean | true/false | Religious site |
| `is_ancient` | boolean | true/false | Ancient ruins |
| `is_ruins` | boolean | true/false | In ruins state |
| `material` | string | stone, brick, wood, iron, concrete | Primary material |
| `architectural_style` | string | gothic, baroque, modern, etc. | Architecture style |
| `purpose` | string | religious, military, residential, etc. | Original purpose |
| `can_enter_inside` | boolean | true/false | Can visitors enter |

---

## Question Data Format

### Schema

```json
{
  "id": "string (required, unique, format: q_NNN)",
  "text": {
    "en": "string (required)",
    "bn": "string (optional)"
  },
  "characteristic": "string (required)",
  "value": "any (string | number | boolean)",
  "operator": "string (optional, default: 'equals')",
  "discriminating_power": "number (0.0-1.0, required)",
  "category": "string (required)",
  "applies_to": "array of strings (optional)",
  "metadata": {
    "added_date": "string (ISO 8601)",
    "times_asked": "number",
    "effectiveness_score": "number (0.0-1.0)"
  }
}
```

### Example Questions

```json
{
  "id": "q_001",
  "text": {
    "en": "Is it in Europe?",
    "bn": "এটি কি ইউরোপে?"
  },
  "characteristic": "continent",
  "value": "europe",
  "operator": "equals",
  "discriminating_power": 0.95,
  "category": "location",
  "applies_to": ["country", "city", "historic_place"],
  "metadata": {
    "added_date": "2026-01-15T00:00:00Z",
    "times_asked": 15420,
    "effectiveness_score": 0.93
  }
}
```

```json
{
  "id": "q_042",
  "text": {
    "en": "Is it a UNESCO World Heritage Site?",
    "bn": "এটি কি ইউনেস্কো ওয়ার্ল্ড হেরিটেজ সাইট?"
  },
  "characteristic": "is_unesco",
  "value": true,
  "operator": "equals",
  "discriminating_power": 0.72,
  "category": "classification",
  "applies_to": ["historic_place", "city"],
  "metadata": {
    "added_date": "2026-01-15T00:00:00Z",
    "times_asked": 8234,
    "effectiveness_score": 0.78
  }
}
```

```json
{
  "id": "q_089",
  "text": {
    "en": "Was it built before 1900?",
    "bn": "এটি কি ১৯০০ সালের আগে নির্মিত হয়েছিল?"
  },
  "characteristic": "built_year",
  "value": 1900,
  "operator": "less_than",
  "discriminating_power": 0.68,
  "category": "temporal",
  "applies_to": ["historic_place"],
  "metadata": {
    "added_date": "2026-01-16T00:00:00Z",
    "times_asked": 5123,
    "effectiveness_score": 0.71
  }
}
```

### Question Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `equals` | Exact match (default) | `continent == "europe"` |
| `not_equals` | Not equal | `is_island != true` |
| `greater_than` | Greater than | `population > 10` |
| `less_than` | Less than | `built_year < 1900` |
| `greater_or_equal` | ≥ | `height >= 300` |
| `less_or_equal` | ≤ | `area <= 1000` |
| `contains` | Array contains | `famous_for contains "wine"` |
| `in_range` | Between values | `population in [1, 10]` |

### Question Categories

| Category | Description | Examples |
|----------|-------------|----------|
| `location` | Geographic location | Continent, country, region |
| `physical` | Physical attributes | Size, material, color |
| `temporal` | Time-related | Age, era, built year |
| `classification` | Type/category | Is monument, is religious |
| `cultural` | Cultural aspects | Language, cuisine, tradition |
| `functional` | Purpose/function | Can enter, has metro |
| `political` | Political status | EU member, capital |
| `natural` | Natural features | Climate, coastline |

---

## Validation Rules

### Place Validation

1. **Required Fields**:
   - `id` (unique, snake_case, no spaces)
   - `name`
   - `type` (must be valid enum)
   - `characteristics` (at least 5)

2. **Characteristic Rules**:
   - At least 5 characteristics required
   - Must include `continent` and `country` (except for countries)
   - Values must match type (string/number/boolean)
   - No null values

3. **Metadata Rules**:
   - `added_date` must be valid ISO 8601
   - `verified` defaults to false

### Question Validation

1. **Required Fields**:
   - `id` (format: `q_NNN` where N is digit)
   - `text.en` (English text required)
   - `characteristic`
   - `discriminating_power` (0.0-1.0)
   - `category`

2. **Text Rules**:
   - English text required
   - Bengali text optional but recommended
   - No HTML or special formatting
   - Clear, concise language

3. **Discriminating Power**:
   - Must be between 0.0 and 1.0
   - Higher = more useful for narrowing down
   - Calculate based on: splits places evenly

### Running Validation

```bash
# Validate all data
python data/scripts/validate_data.py

# Validate specific file
python data/scripts/validate_data.py --file data/places/countries.json

# Verbose output
python data/scripts/validate_data.py --verbose
```

---

## Data Management Scripts

### Generate Data

```bash
# Generate new places using AI
python data/scripts/generate_data.py --type country --count 10

# Generate questions
python data/scripts/generate_data.py --type question --count 20
```

### Combine Data

```bash
# Combine all place files into combined.json
python data/scripts/combine_data.py
```

### Enhance Data

```bash
# Add missing characteristics to existing places
python data/scripts/enhance_data.py --auto-fill

# Recalculate discriminating power
python data/scripts/enhance_data.py --recalculate-power
```

---

## Best Practices

### Adding New Places

1. **Research thoroughly**: Ensure accuracy
2. **Add comprehensive characteristics**: More = better
3. **Use consistent naming**: Follow existing patterns
4. **Provide metadata**: Help future contributors
5. **Validate before commit**: Run validation script

### Adding New Questions

1. **Test discriminating power**: Should split places well
2. **Make it clear**: No ambiguous wording
3. **Provide translations**: At least English + Bengali
4. **Choose appropriate category**: Helps organization
5. **Test with real places**: Verify it works

### Updating Existing Data

1. **Document changes**: Update `last_updated`
2. **Add to contributors**: Credit yourself
3. **Maintain backward compatibility**: Don't break existing questions
4. **Re-validate**: Ensure still valid

---

## Data Statistics

Current dataset size (as of Feb 2026):

| Type | Count | Avg Characteristics |
|------|-------|-------------------|
| Countries | 195+ | 15 |
| Cities | 300+ | 12 |
| Historic Places | 250+ | 14 |
| Questions | 350+ | - |

**Total Places**: 745+  
**Total Questions**: 350+  
**Characteristics Coverage**: 85%+

---

## JSON Schema Files

Full JSON schemas available in `data/schema/`:

- `place_schema.json` - Place data schema
- `question_schema.json` - Question data schema

Validate against schema:
```bash
jsonschema -i data/places/countries.json data/schema/place_schema.json
```

---

## Examples Repository

See `data/examples/` for:
- Sample places for each type
- Sample questions for each category
- Edge cases and special scenarios
- Testing fixtures

---

## Future Enhancements

Planned improvements to data format:

1. **Relationships**: Link related places (e.g., Eiffel Tower → Paris → France)
2. **Multilingual**: Support for more languages
3. **Rich Media**: Multiple images, videos, 3D models
4. **User Contributions**: Community-submitted places
5. **Versioning**: Track data changes over time
6. **Quality Scores**: Rate data quality and coverage

---

## Questions?

For questions about data format:
- Check examples in `data/examples/`
- Read validation script source
- Open a discussion on GitHub
- See [CONTRIBUTING.md](CONTRIBUTING.md)

---

**Last Updated**: February 2026