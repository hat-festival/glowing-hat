import json
from pathlib import Path
from unittest import TestCase

import redis
import yaml

from lib.custodian import Custodian


class TestCustodian(TestCase):
    """Test the Custodian."""

    def setUp(self):
        """Setup."""  # noqa: D401
        self.redis = redis.Redis()
        self.redis.flushdb()

    def test_init(self):
        """Test it constructs."""
        cus = Custodian("test")

        self.assertEqual(cus.namespace, "test")  # noqa: PT009

    def test_add_to_hoop(self):
        """Test we can add an item to a hoop."""
        cus = Custodian("test")
        cus.add_item_to_hoop("apple", "fruit")

        self.assertEqual(  # noqa: PT009
            self.redis.lrange("test:hoop:fruit", 0, -1)[0].decode(), "apple"
        )

    def test_add_more_to_hoop(self):
        """Test we can add several items to a hoop."""
        cus = Custodian("test")
        cus.add_item_to_hoop("apple", "fruit")
        cus.add_item_to_hoop("banana", "fruit")
        cus.add_item_to_hoop("clementine", "fruit")

        self.assertEqual(  # noqa: PT009
            list(  # noqa: C417
                map(
                    lambda x: x.decode(),
                    self.redis.lrange("test:hoop:fruit", 0, -1),
                )
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

        self.assertEqual(  # noqa: PT009
            list(  # noqa: C417
                map(
                    lambda x: x.decode(),
                    self.redis.lrange("test:hoop:fruit", 0, -1),
                )
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

        self.assertEqual(cus.get("fruit"), "apple")  # noqa: PT009
        self.assertEqual(  # noqa: PT009
            list(  # noqa: C417
                map(
                    lambda x: x.decode(),
                    self.redis.lrange("test:hoop:fruit", 0, -1),
                )
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

        self.assertEqual(  # noqa: PT009
            list(  # noqa: C417
                map(
                    lambda x: json.loads(x.decode()),
                    self.redis.lrange("test:hoop:colour", 0, -1),
                )
            ),
            [[255, 255, 0], [255, 0, 255], [0, 255, 255]],
        )

        self.assertEqual(cus.get("colour"), [255, 255, 0])  # noqa: PT009

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
            self.assertEqual(cus.get(key), expected)  # noqa: PT009

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

    def test_unsetting(self):
        """Test it unsets something."""
        cus = Custodian("test")
        cus.add_item_to_hoop("apple", "fruit")
        cus.add_item_to_hoop("banana", "fruit")
        cus.add_item_to_hoop("clementine", "fruit")

        self.assertEqual(  # noqa: PT009
            list(  # noqa: C417
                map(
                    lambda x: x.decode(),
                    self.redis.lrange("test:hoop:fruit", 0, -1),
                )
            ),
            ["clementine", "banana", "apple"],
        )

        cus.unset("hoop:fruit")
        self.assertIsNone(cus.get("hoop:fruit"))  # noqa: PT009

    def test_reset_colour_sources(self):
        """Test it resets the colour-sources."""
        conf = yaml.safe_load(
            Path("tests/fixtures/custodian/defaults.yaml").read_text(encoding="UTF-8")
        )
        cus = Custodian("test", conf=conf)
        cus.populate()

        cus.reset_colour_sources(["wheel", "redis"])
        self.assertEqual(  # noqa: PT009
            list(  # noqa: C417
                map(
                    lambda x: x.decode(),
                    self.redis.lrange("test:hoop:colour-source", 0, -1),
                )
            ),
            ["redis", "wheel"],
        )

    def test_rotate_until(self):
        """Test it rotates-until."""
        cus = Custodian("test")
        cus.add_item_to_hoop("aardvark", "animal")
        cus.add_item_to_hoop("baboon", "animal")
        cus.add_item_to_hoop("cuttlefish", "animal")
        cus.add_item_to_hoop("dog", "animal")
        cus.add_item_to_hoop("elephant", "animal")
        cus.add_item_to_hoop("fruitbat", "animal")

        cus.rotate_until("animal", "dog")
        self.assertEqual(cus.get("animal"), "dog")  # noqa: PT009

    def test_get_and_reset(self):
        """Test it gets and resets."""
        cus = Custodian("test")
        cus.set("banana", 2)
        result = cus.get_and_reset("banana")

        self.assertEqual(result, 2)  # noqa: PT009
        self.assertEqual(cus.get("banana"), 0)  # noqa: PT009

    def test_get_and_reset_with_default(self):
        """Test it gets and resets to a specified default."""
        cus = Custodian("test")
        cus.set("name", "dave")
        result = cus.get_and_reset("name", "steve")

        self.assertEqual(result, "dave")  # noqa: PT009
        self.assertEqual(cus.get("name"), "steve")  # noqa: PT009

    def test_increment(self):
        """Test it increments a value."""
        cus = Custodian("test")
        cus.set("score", 3)
        cus.increment("score")
        self.assertEqual(cus.get("score"), 4)  # noqa: PT009

    def test_decrement(self):
        """Test it decrements a value."""
        cus = Custodian("test")
        cus.set("score", 0)
        cus.decrement("score")
        self.assertEqual(cus.get("score"), -1)  # noqa: PT009
