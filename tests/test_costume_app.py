from costume_app import Costume, CostumePredictor, InventoryManager


def test_inventory_add_and_update_stock(tmp_path):
    db = tmp_path / "inventory.json"
    manager = InventoryManager(str(db))

    manager.add_costume(
        Costume(
            name="Forest Elf",
            category="fantasy",
            theme="nature",
            weather="mild",
            event_type="festival",
            stock=2,
            rental_price=40.0,
        )
    )

    assert len(manager.list_costumes()) == 1
    assert manager.update_stock("Forest Elf", 7) is True
    assert manager.list_costumes()[0].stock == 7
    assert manager.update_stock("Unknown", 3) is False


def test_predictor_ranks_matching_costumes_first():
    predictor = CostumePredictor()
    inventory = [
        Costume("Winter Witch", "fantasy", "magic", "cold", "halloween", 4, 48.0),
        Costume("Summer Pirate", "adventure", "ocean", "hot", "party", 3, 20.0),
        Costume("Classic Vampire", "horror", "gothic", "cold", "halloween", 1, 35.0),
    ]

    profile = {
        "event_type": "halloween",
        "weather": "cold",
        "theme": "gothic",
        "budget": "40",
    }

    recommendations = predictor.predict(profile, inventory)

    assert recommendations
    assert recommendations[0].name == "Classic Vampire"
    assert all(item.stock > 0 for item in recommendations)
