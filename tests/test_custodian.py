import json
from pathlib import Path
from unittest import TestCase

import redis
import yaml

from lib.custodian import Custodian


class TestCustodian(TestCase):
    """Test the Custodian."""

    def setUp(self):
        """Setup."""
        self.redis = redis.Redis()
        self.redis.flushdb()

    def test_init(self):
        """Test it constructs."""
        cus = Custodian("test")

        self.assertEqual(cus.namespace, "test")

    def test_add_to_hoop(self):
        """Test we can add an item to a hoop."""
        cus = Custodian("test")
        cus.add_item_to_hoop("apple", "fruit")

        self.assertEqual(
            self.redis.lrange("test:hoop:fruit", 0, -1)[0].decode(), "apple"
        )

    def test_add_more_to_hoop(self):
        """Test we can add several items to a hoop."""
        cus = Custodian("test")
        cus.add_item_to_hoop("apple", "fruit")
        cus.add_item_to_hoop("banana", "fruit")
        cus.add_item_to_hoop("clementine", "fruit")

        self.assertEqual(
            list(
                map(lambda x: x.decode(), self.redis.lrange("test:hoop:fruit", 0, -1))
            ),
            ["clementine", "banana", "apple"],
        )

    def test_no_multiples(self):
        """Test that the list is unique."""
        cus = Custodian("test")
        cus.add_item_to_hoop("apple", "fruit")
        cus.add_item_to_hoop("banana", "fruit")
        cus.add_item_to_hoop("clementine", "fruit")
        cus.add_item_to_hoop("banana", "fruit")
        cus.add_item_to_hoop("banana", "fruit")

        self.assertEqual(
            list(
                map(lambda x: x.decode(), self.redis.lrange("test:hoop:fruit", 0, -1))
            ),
            ["clementine", "banana", "apple"],
        )

    def test_rotate_hoop(self):
        """Test we can select the `next` item from the hoop and rotate it."""
        cus = Custodian("test")
        cus.add_item_to_hoop("apple", "fruit")
        cus.add_item_to_hoop("banana", "fruit")
        cus.add_item_to_hoop("clementine", "fruit")

        cus.next("fruit")

        self.assertEqual(cus.get("fruit"), "apple")
        self.assertEqual(
            list(
                map(lambda x: x.decode(), self.redis.lrange("test:hoop:fruit", 0, -1))
            ),
            ["apple", "clementine", "banana"],
        )

    def test_load_colour_set(self):
        """Test it loads-in a colour-set."""
        cus = Custodian("test")
        cus.set("colour-source", "redis")
        first_colours = {
            "red": [255, 0, 0],
            "green": [0, 255, 0],
            "blue": [0, 0, 255],
        }
        cus.load_colour_set(first_colours)

        colours = {
            "yellow": [255, 255, 0],
            "cyan": [0, 255, 255],
            "magenta": [255, 0, 255],
        }
        cus.load_colour_set(colours)

        self.assertEqual(
            list(
                map(
                    lambda x: json.loads(x.decode()),
                    self.redis.lrange("test:hoop:colour", 0, -1),
                )
            ),
            [[255, 255, 0], [255, 0, 255], [0, 255, 255]],
        )

        self.assertEqual(cus.get("colour"), [255, 255, 0])

    def test_populating(self):
        """Test it populates with initial values."""
        conf = yaml.safe_load(
            Path("tests/fixtures/custodian/defaults.yaml").read_text(encoding="UTF-8")
        )
        cus = Custodian("test", conf=conf)
        cus.populate()

        expecteds = (
            ("colour-source", "wheel"),
            ("colour-set", "rgb"),
            ("colour", [255, 0, 0]),
            ("axis", "x"),
            ("invert", False),
        )

        for key, expected in expecteds:
            self.assertEqual(cus.get(key), expected)

    def test_triggering(self):
        """Test a new colour-set triggers a reload."""
        conf = yaml.safe_load(
            Path("tests/fixtures/custodian/defaults.yaml").read_text(encoding="UTF-8")
        )
        cus = Custodian("test", conf=conf)
        cus.populate()

        # self.assertEqual(cus.get("colour"), [255, 0, 0])
        # cus.next("colour-set")
        # cus.next("colour")
        # self.assertEqual(cus.get("colour"), [246, 138, 30])
