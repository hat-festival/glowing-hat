from unittest import TestCase

import redis

from glowing_hat.custodian import Custodian


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
