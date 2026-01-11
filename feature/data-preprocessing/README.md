# Branch: feature/data-preprocessing

## Purpose
Clean and prepare Amazon product review data for the recommendation system.

## Files
- `data_preprocessing.py` - Main preprocessing pipeline
- `requirements.txt` - Python dependencies
- `tests/test_preprocessing.py` - Unit tests
- `README.md` - This file

## Key Features
- Removes duplicates and handles missing values
- Parses JSON price and category fields
- Creates aggregated user/product features
- Validates data quality
- Saves cleaned dataset with summary statistics

## Usage

```bash
python data_preprocessing.py
pytest tests/test_preprocessing.py
```

## Testing
Run tests with:
```bash
pytest tests/test_preprocessing.py -v
```

