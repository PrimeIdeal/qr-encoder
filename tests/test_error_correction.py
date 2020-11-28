from collections import Counter

from encode.error_correction import _create_stores


class TestCreateStores:

    def test_log_domain(self):
        _, test_store = _create_stores()

        assert set(test_store.keys()) == set(k for k in range(1, 256))

    def test_log_image_values(self):
        _, test_store = _create_stores()

        assert set(test_store.values()) == set(k for k in range(255))

    def test_log_image_counts(self):
        _, test_store = _create_stores()
        image_count = Counter(test_store.values())

        assert set(image_count.values()) == {1}

    def test_exp_domain(self):
        test_store, _ = _create_stores()

        assert set(test_store.keys()) == set(k for k in range(256))

    def test_exp_image_values(self):
        test_store, _ = _create_stores()

        assert set(test_store.values()) == set(k for k in range(1, 256))

    def test_exp_image_counts(self):
        test_store, _ = _create_stores()
        image_count = Counter(test_store.values())

        assert set(image_count.values()) == {1, 2}

        image_count.pop(1)

        assert set(image_count.values()) == {1}
