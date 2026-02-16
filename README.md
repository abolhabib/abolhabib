# Costume Prediction and Management App

A lightweight Python application for:
- Managing costume inventory (add, list, and update stock).
- Predicting recommended costumes from user preferences.
- Persisting data locally using JSON storage.

## Features

- **Inventory management**
  - Add new costumes.
  - View available costumes.
  - Update stock counts.
- **Prediction engine**
  - Recommends costumes based on:
    - event type
    - weather
    - theme
    - budget
- **Persistent storage**
  - Saves data into `inventory.json` automatically.

## Project structure

- `costume_app.py` — application logic and CLI entry point.
- `tests/test_costume_app.py` — unit tests for inventory and prediction logic.

## Requirements

- Python 3.9+

## Run the app

```bash
python costume_app.py
```

## Run tests

```bash
python -m pytest -q
```

## Example use case

1. Start the app.
2. Add costumes for your store.
3. Run prediction for a customer profile (e.g., *Halloween*, *cold weather*, *gothic theme*, budget *40*).
4. Use recommendations to suggest outfits and manage rental stock.
