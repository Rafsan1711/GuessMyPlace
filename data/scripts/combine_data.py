#!/usr/bin/env python3
"""
Combine Data Script for GuessMyPlace
Combines all place data files into a single combined.json file
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_success(msg: str):
    print(f"{Colors.GREEN}✓{Colors.END} {msg}")


def print_error(msg: str):
    print(f"{Colors.RED}✗{Colors.END} {msg}")


def print_info(msg: str):
    print(f"{Colors.BLUE}ℹ{Colors.END} {msg}")


def load_json_file(file_path: Path) -> List[Dict]:
    """Load a JSON file and return data"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print_success(f"Loaded {file_path.name}: {len(data)} items")
        return data
    except FileNotFoundError:
        print_error(f"File not found: {file_path.name}")
        return []
    except json.JSONDecodeError as e:
        print_error(f"Invalid JSON in {file_path.name}: {e}")
        return []


def combine_places(data_dir: Path) -> bool:
    """Combine all place files into combined.json"""
    print("\n" + "="*60)
    print("Combining Place Data Files")
    print("="*60 + "\n")
    
    # Load individual files
    countries = load_json_file(data_dir / 'places' / 'countries.json')
    cities = load_json_file(data_dir / 'places' / 'cities.json')
    historic_places = load_json_file(data_dir / 'places' / 'historic_places.json')
    
    # Combine all data
    combined = countries + cities + historic_places
    
    # Check for duplicate IDs
    ids = [place['id'] for place in combined]
    duplicates = [id for id in ids if ids.count(id) > 1]
    
    if duplicates:
        print_error(f"Duplicate IDs found: {set(duplicates)}")
        return False
    
    # Add metadata
    combined_data = {
        "metadata": {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "total_places": len(combined),
            "countries": len(countries),
            "cities": len(cities),
            "historic_places": len(historic_places)
        },
        "places": combined
    }
    
    # Write combined file
    output_file = data_dir / 'places' / 'combined.json'
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(combined_data, f, indent=2, ensure_ascii=False)
        
        print_success(f"Combined file created: {output_file.name}")
        print_info(f"Total places: {len(combined)}")
        print_info(f"  - Countries: {len(countries)}")
        print_info(f"  - Cities: {len(cities)}")
        print_info(f"  - Historic Places: {len(historic_places)}")
        
        return True
        
    except Exception as e:
        print_error(f"Failed to write combined file: {e}")
        return False


def main():
    """Main entry point"""
    # Get data directory
    script_dir = Path(__file__).parent
    data_dir = script_dir.parent
    
    # Combine data
    success = combine_places(data_dir)
    
    # Exit with appropriate code
    if success:
        print("\n" + Colors.GREEN + "✨ Data combination complete!" + Colors.END + "\n")
        sys.exit(0)
    else:
        print("\n" + Colors.RED + "❌ Data combination failed!" + Colors.END + "\n")
        sys.exit(1)


if __name__ == '__main__':
    main()