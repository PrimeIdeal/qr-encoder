from collections import Counter
from unittest.mock import patch, Mock

import pytest

from encode.error_correction import _create_stores, ErrorCorrector


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


class TestConstructor:

    @patch(
        'encode.error_correction._create_stores',
        side_effect=lambda: (Mock(), Mock())
    )
    def test_store_creation(self, mock_create_stores):
        ErrorCorrector((26, 3, 44, 11, 45))

        mock_create_stores.assert_called_once()

    @pytest.mark.parametrize(
        'block_info, expected',
        [
            ((26, 17, 42, None, None), (442, 714)),
            ((30, 7, 24, 22, 25), (870, 718))
        ],
        ids=[
            'Single group',
            'Two groups'
        ]
    )
    def test_num_bytes(self, block_info, expected):
        test_corrector = ErrorCorrector(block_info)
        expected_ec, expected_msg = expected

        assert test_corrector.num_correction_bytes == expected_ec
        assert test_corrector.num_message_bytes == expected_msg
