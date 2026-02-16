"""Costume prediction and management application.

This module contains a small, self-contained application that can:
1. Manage costume inventory.
2. Predict suitable costumes from user preferences.
3. Persist inventory to a local JSON file.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Dict, List


@dataclass
class Costume:
    """Represents one costume style tracked by the application."""

    name: str
    category: str
    theme: str
    weather: str
    event_type: str
    stock: int
    rental_price: float


class InventoryManager:
    """Simple JSON-backed inventory manager for costumes."""

    def __init__(self, storage_path: str = "inventory.json") -> None:
        self.storage_path = Path(storage_path)
        self._inventory: Dict[str, Costume] = {}
        self.load()

    def add_costume(self, costume: Costume) -> None:
        self._inventory[costume.name.lower()] = costume
        self.save()

    def list_costumes(self) -> List[Costume]:
        return sorted(self._inventory.values(), key=lambda c: c.name)

    def update_stock(self, costume_name: str, stock: int) -> bool:
        key = costume_name.lower()
        if key not in self._inventory:
            return False
        self._inventory[key].stock = stock
        self.save()
        return True

    def available_costumes(self) -> List[Costume]:
        return [c for c in self._inventory.values() if c.stock > 0]

    def save(self) -> None:
        payload = [asdict(costume) for costume in self._inventory.values()]
        self.storage_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def load(self) -> None:
        if not self.storage_path.exists():
            return
        raw = self.storage_path.read_text(encoding="utf-8").strip()
        if not raw:
            return
        data = json.loads(raw)
        self._inventory = {
            record["name"].lower(): Costume(**record)
            for record in data
        }


class CostumePredictor:
    """Rule-based prediction engine for selecting costumes."""

    def predict(self, profile: Dict[str, str], inventory: List[Costume]) -> List[Costume]:
        event_type = profile.get("event_type", "").lower().strip()
        weather = profile.get("weather", "").lower().strip()
        theme = profile.get("theme", "").lower().strip()
        budget = float(profile.get("budget", 10_000))

        scored: List[tuple[int, Costume]] = []
        for costume in inventory:
            score = 0
            if costume.event_type.lower() == event_type:
                score += 3
            if costume.weather.lower() == weather:
                score += 2
            if costume.theme.lower() == theme:
                score += 2
            if costume.rental_price <= budget:
                score += 2
            if costume.stock > 0:
                score += 1
            scored.append((score, costume))

        scored.sort(key=lambda item: (item[0], -item[1].rental_price), reverse=True)
        return [costume for score, costume in scored if score >= 4 and costume.stock > 0][:5]


def seed_inventory_if_empty(manager: InventoryManager) -> None:
    if manager.list_costumes():
        return

    starter_costumes = [
        Costume("Classic Vampire", "horror", "gothic", "cold", "halloween", 8, 35.0),
        Costume("Galaxy Explorer", "sci-fi", "space", "mild", "party", 5, 42.0),
        Costume("Royal Pharaoh", "historical", "egypt", "hot", "festival", 3, 55.0),
        Costume("Winter Witch", "fantasy", "magic", "cold", "halloween", 4, 48.0),
        Costume("Pirate Captain", "adventure", "ocean", "mild", "birthday", 6, 30.0),
    ]

    for costume in starter_costumes:
        manager.add_costume(costume)


def print_costumes(costumes: List[Costume]) -> None:
    if not costumes:
        print("No costumes found.")
        return

    for idx, costume in enumerate(costumes, start=1):
        print(
            f"{idx}. {costume.name} | event={costume.event_type} | theme={costume.theme} "
            f"| weather={costume.weather} | stock={costume.stock} | price=${costume.rental_price:.2f}"
        )


def run_cli() -> None:
    manager = InventoryManager()
    seed_inventory_if_empty(manager)
    predictor = CostumePredictor()

    while True:
        print("\n=== Costume Prediction & Management ===")
        print("1) List inventory")
        print("2) Add costume")
        print("3) Update stock")
        print("4) Predict costume")
        print("5) Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            print_costumes(manager.list_costumes())

        elif choice == "2":
            costume = Costume(
                name=input("Name: ").strip(),
                category=input("Category (e.g. fantasy/horror): ").strip(),
                theme=input("Theme: ").strip(),
                weather=input("Weather (hot/mild/cold): ").strip(),
                event_type=input("Event type (halloween/party/festival): ").strip(),
                stock=int(input("Stock: ").strip()),
                rental_price=float(input("Rental price: ").strip()),
            )
            manager.add_costume(costume)
            print("Costume saved.")

        elif choice == "3":
            name = input("Costume name to update: ").strip()
            stock = int(input("New stock: ").strip())
            if manager.update_stock(name, stock):
                print("Stock updated.")
            else:
                print("Costume not found.")

        elif choice == "4":
            profile = {
                "event_type": input("Event type: ").strip(),
                "weather": input("Weather: ").strip(),
                "theme": input("Theme: ").strip(),
                "budget": input("Budget: ").strip(),
            }
            recommendations = predictor.predict(profile, manager.available_costumes())
            print("\nTop recommendations:")
            print_costumes(recommendations)

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose from 1-5.")


if __name__ == "__main__":
    run_cli()
