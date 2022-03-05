import json
import unittest

import numpy as np
import pandas as pd

from .. import utils


class TestUtilsParsing(unittest.TestCase):
    """Test the utils (from backtesting_results) functions"""

    def setUp(self) -> None:
        path = "C:/Users/Gabriele/Desktop/X/backtesting_results/test/mock.json"
        with open(path, mode="r", encoding="utf-8") as f:
            self.mock_data = json.load(f)
        return super().setUp()

    def test_get_executed_orders_normal_len(self):
        length_result = len(utils.get_executed_orders(self.mock_data[1]))
        self.assertEqual(length_result, 3)

    def test_get_executed_orders_ignore_sl_len(self):
        data = self.mock_data[1]
        length_result = len(utils.get_executed_orders(data, ignore=["SL"]))
        self.assertEqual(length_result, 2)

    def test_get_executed_orders_first_result_type(self):
        result_type = utils.get_executed_orders(self.mock_data[1])[0]["name"]
        self.assertEqual(result_type, "SL")

    def test_get_executed_orders_first_result_price(self):
        price = utils.get_executed_orders(self.mock_data[1])[0]["execution"]["price"]
        self.assertAlmostEqual(price, 135.55)

    def test_determine_position_result_eop_time(self):
        data = self.mock_data[0]
        time = utils.determine_position_result(data, partials=[1], ignore=["SL"])[0]
        self.assertEqual(time, pd.to_datetime("2020-11-05 17:29:00+00:00", utc=True))

    def test_determine_position_result_eop_r(self):
        data = self.mock_data[0]
        r = utils.determine_position_result(data, partials=[1], ignore=["SL"])[1]
        self.assertAlmostEqual(r, -0.118 / 0.259)

    def test_determine_position_result_sl_r(self):
        data = self.mock_data[0]
        r = utils.determine_position_result(data, partials=[1], ignore=[])[1]
        self.assertAlmostEqual(r, -1)

    def test_determine_position_result_sl_r_wrong(self):
        data = self.mock_data[0]
        r = utils.determine_position_result(data, partials=[1], ignore=[])[1]
        self.assertNotAlmostEqual(r, 1)

    def test_determine_position_result_tp_r(self):
        data = self.mock_data[1]
        r = utils.determine_position_result(data, partials=[1], ignore=["SL"])[1]
        self.assertAlmostEqual(r, 0.1425 / 0.137)

    def test_determine_position_result_tp_r_partials(self):
        data = self.mock_data[1]
        part = [0.6, 0.4]
        r = utils.determine_position_result(data, partials=part, ignore=["SL"])[1]
        self.assertAlmostEqual(r, 0.6 * (0.1425 / 0.137) + 0.4 * (0.2625 / 0.137))

    def test_determine_position_result_tp_r_partials_wrong(self):
        data = self.mock_data[1]
        part = [0.6, 0.4]
        r = utils.determine_position_result(data, partials=part, ignore=["SL"])[1]
        self.assertNotAlmostEqual(r, -1)

    def test_get_position_tps_long(self):
        data = self.mock_data[0]
        tps = utils.get_position_tps(data)
        self.assertListEqual(tps, [136.13, 136.6])

    def test_get_position_tps_short(self):
        data = self.mock_data[3]
        tps = utils.get_position_tps(data)
        self.assertListEqual(tps, [135.85, 135.5, 135.4, 135.1, 134.1])

    def test_find_better_sl_nan(self):
        data = self.mock_data[0]
        self.assertTrue(np.isnan(utils.find_better_sl(data)))

    def test_find_better_sl(self):
        data = self.mock_data[1]
        self.assertAlmostEqual(utils.find_better_sl(data), 135.514)

    def test_find_better_tp_nan(self):
        data = self.mock_data[0]
        self.assertTrue(np.isnan(utils.find_better_tp(data)))

    def test_find_better_tp(self):
        data = self.mock_data[1]
        self.assertAlmostEqual(utils.find_better_tp(data), 135.751)


if __name__ == "__main__":
    unittest.main()
