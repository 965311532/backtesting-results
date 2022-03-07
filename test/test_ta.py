import unittest

import pandas as pd

from .. import utils


class TestUtilsTA(unittest.TestCase):
    """Test class for testing data manipulation and Technical Analysis"""

    def setUp(self) -> None:
        self.date_range1 = pd.date_range(start="2020-2-1", periods=10, freq="1H")
        self.date_range2 = pd.date_range(start="2020-2-1", periods=10, freq="2H")
        return super().setUp()

    def test_merge_empty(self):
        x = utils.merge(
            {
                "0": pd.DataFrame(index=self.date_range1),
                "1": pd.DataFrame(index=self.date_range2),
            }
        )
        self.assertEqual(len(x), 0)

    def test_merge_all_1(self):
        df0 = pd.DataFrame(index=self.date_range1)
        df1 = pd.DataFrame(index=self.date_range2)
        df0["col"] = df1["col"] = 1
        merged = utils.merge({"0": df0, "1": df1})
        with self.subTest("Column names"):
            self.assertListEqual(merged.columns.tolist(), ["col_0", "col_1"])
        with self.subTest("Sum of col_0"):
            self.assertEqual(merged.col_0.sum(), df0.col.sum())
        with self.subTest("Sum of col_1"):
            self.assertEqual(merged.col_1.sum(), df1.col.sum())
        with self.subTest("The sum of the two cols should be 2"):
            self.assertEqual(merged.iloc[0].sum(), 2)

    def test_drawdown(self):
        results = [-1, -1, -1, -1, 1, 1, -1, 1, -1]
        df = pd.DataFrame(results, columns=["result"])
        self.assertEqual(utils.drawdown(df).dd.min(), -4)

    def test_reduce_daily_trades_instance(self):
        date_range = pd.date_range(start="2020-1-1", freq="3H", periods=24)
        df = pd.DataFrame([1] * 24, index=date_range, columns=["col"])
        self.assertIsInstance(utils.reduce_daily_trades(df, 3), pd.DataFrame)

    def test_reduce_daily_trades(self):
        date_range = pd.date_range(start="2020-1-1", freq="3H", periods=24)
        df = pd.DataFrame([1] * 24, index=date_range, columns=["col"])
        # If we reduce from 8 to 6 over 3 days, len should be 6*3=18
        self.assertEqual(len(utils.reduce_daily_trades(df, 6)), 18)

    def test_add_open_trades(self):
        date_range_open = pd.date_range(start="2020-1-1", freq="1H", periods=10)
        date_range_close = pd.date_range(start="2020-1-1 00:05", freq="2H", periods=10)
        df = pd.DataFrame({"open": date_range_open, "close": date_range_close})
        self.assertListEqual(
            utils.add_open_trades(df).open_trades.tolist(),
            [1, 1, 2, 2, 3, 3, 4, 4, 5, 5],
        )

    def test_add_streak(self):
        results = [-1, -0.05, -1, 1, 1, -0.05, 1, -1]
        df = pd.DataFrame(results, columns=["result"])
        self.assertListEqual(
            utils.add_streak(df, tolerance=0.1).streak.tolist(),
            [-1, -2, -3, 1, 2, 3, 4, -1],
        )

    def test_make_streaks_df_by_open_all_zeros(self):
        results = [-1, -0.05, -1, 1, 1, -0.05, 1, -1, -1, -1]
        date_range_open = pd.date_range(start="2020-1-1", freq="1H", periods=10)
        date_range_close = pd.date_range(start="2020-1-1 01:05", freq="2H", periods=10)
        df = pd.DataFrame(
            {"open": date_range_open, "close": date_range_close, "result": results}
        )
        self.assertListEqual(
            utils.make_streaks_df_by_open(df).streak_at_open.tolist(), [0] * 10
        )

    def test_make_streaks_df_by_open(self):
        results = [-1, -0.05, -1, 1, 1, -0.05, 1, -1, -1, -1]
        date_range_open = pd.date_range(start="2020-1-1", freq="1H", periods=10)
        date_range_close = pd.date_range(start="2020-1-1 00:05", freq="75T", periods=10)
        df = pd.DataFrame(
            {"open": date_range_open, "close": date_range_close, "result": results}
        )
        self.assertListEqual(
            utils.make_streaks_df_by_open(df).streak_at_open.tolist(),
            [0, -1, -2, -3, 1, 0, 0, 0, 0, 0],
        )

    def test_make_streaks_df_by_close(self):

        results = [-1, -0.05, -1, 1, 1, -0.05, 1, -1, -1, -1]
        date_range_open = pd.date_range(start="2020-1-1", freq="1H", periods=10)
        date_range_close = pd.date_range(start="2020-1-1 00:05", freq="75T", periods=10)
        df = pd.DataFrame(
            {"open": date_range_open, "close": date_range_close, "result": results}
        )
        self.assertListEqual(
            utils.make_streaks_df_by_close(df).streak.tolist(),
            [-1, -2, -3, 1, 2, 3, 4, -1, -2, -3],
        )

    def test_make_streaks_df_by_close_streak_max(self):

        results = [-1, -0.05, -1, 1, 1, -0.05, 1, -1, -1, -1]
        date_range_open = pd.date_range(start="2020-1-1", freq="1H", periods=10)
        date_range_close = pd.date_range(start="2020-1-1 00:05", freq="75T", periods=10)
        df = pd.DataFrame(
            {"open": date_range_open, "close": date_range_close, "result": results}
        )
        # The reson we don't account for the last streak is that it's technically
        # not finished until another streak starts
        self.assertListEqual(
            utils.make_streaks_df_by_close(df).streak_max.tolist(),
            [bool(x) for x in [0, 0, 1, 0, 0, 0, 1, 0, 0, 0]],
        )

    def test_get_streak_runs(self):

        results = [-1, -0.05, -1, 1, 1, -0.05, 1, -1, -1, -1]
        date_range_open = pd.date_range(start="2020-1-1", freq="1H", periods=10)
        date_range_close = pd.date_range(start="2020-1-1 00:05", freq="75T", periods=10)
        df = pd.DataFrame(
            {"open": date_range_open, "close": date_range_close, "result": results}
        )
        self.assertListEqual(
            utils.get_streak_runs(df.set_index("close")).streak_runs.tolist(),
            [-3, 4],
        )

    def test_map_risk_to_streak(self):
        results = [-1, -0.05, -1, 1, 1, -0.05, 1, -1, -1, -1]
        date_range_open = pd.date_range(start="2020-1-1", freq="1H", periods=10)
        date_range_close = pd.date_range(start="2020-1-1 00:05", freq="75T", periods=10)
        df = pd.DataFrame(
            {"open": date_range_open, "close": date_range_close, "result": results}
        )
        risk = {-1: 0.5, 1: 2}
        self.assertListEqual(
            utils.map_risk_to_streak(df, risk, default=1).risk.tolist(),
            [1, 0.5, 1, 1, 2, 1, 1, 1, 1, 1],
        )

    def test_result_given_risk(self):
        date_range_open = pd.date_range(start="2020-1-1", freq="1H", periods=5)
        date_range_close = pd.date_range(start="2020-1-1 00:05", freq="1H", periods=5)
        results = [-1, 1, 1.5, -0.05, 0.8]
        df = pd.DataFrame(
            {"open": date_range_open, "close": date_range_close, "result": results}
        )
        risk = {-1: 0.5, 2: 2}
        df = utils.map_risk_to_streak(df, risk, default=1)
        # CAREFUL. This is correct, because map_risk_to_streak takes care of streaks
        # by ordering them by open. This makes sure that when the risk is associated
        # to the risk, it's not backwards looking. That's because make_streaks_df_by_open
        # maps the streak AT the open, which, for example, for the first trade is 0.
        self.assertListEqual(
            utils.result_by_close_given_risk(df).result.tolist(),
            [-1, 0.5, 1.5, -0.1, 0.8],
        )

    def test_challenge_pass_all_fail_max_dd(self):
        periods = 400
        date_range_open = pd.date_range(start="2020-1-1", freq="1B", periods=periods)
        date_range_close = pd.date_range(
            start="2020-1-1 00:05", freq="1B", periods=periods
        )
        results = [-1] * periods
        df = pd.DataFrame(
            {"open": date_range_open, "close": date_range_close, "result": results}
        )
        passed = utils.challenge_pass(df)
        self.assertTrue((passed["pass"] == "failed").all())

    def test_challenge_pass_all_fail_max_daily_dd(self):
        periods = 400
        date_range_open = pd.date_range(start="2020-1-1", freq="1B", periods=periods)
        date_range_close = pd.date_range(
            start="2020-1-1 00:05", freq="1B", periods=periods
        )
        results = [-6] * periods
        df = pd.DataFrame(
            {"open": date_range_open, "close": date_range_close, "result": results}
        )
        passed = utils.challenge_pass(df)
        self.assertTrue((passed["pass"] == "failed").all())

    def test_challenge_pass_all_fail_end_in_loss(self):
        periods = 400
        date_range_open = pd.date_range(start="2020-1-1", freq="1B", periods=periods)
        date_range_close = pd.date_range(
            start="2020-1-1 00:05", freq="1B", periods=periods
        )
        results = [-0.01] * periods
        df = pd.DataFrame(
            {"open": date_range_open, "close": date_range_close, "result": results}
        )
        passed = utils.challenge_pass(df)
        self.assertTrue((passed["pass"] == "failed").all())

    def test_challenge_pass_all_pass(self):
        periods = 400
        date_range_open = pd.date_range(start="2020-1-1", freq="1B", periods=periods)
        date_range_close = pd.date_range(
            start="2020-1-1 00:05", freq="1B", periods=periods
        )
        results = [10] * periods
        df = pd.DataFrame(
            {"open": date_range_open, "close": date_range_close, "result": results}
        )
        passed = utils.challenge_pass(df)
        self.assertTrue((passed["pass"] == "passed").all())

    def test_challenge_pass_all_not_failed(self):
        periods = 400
        date_range_open = pd.date_range(start="2020-1-1", freq="1B", periods=periods)
        date_range_close = pd.date_range(
            start="2020-1-1 00:05", freq="1B", periods=periods
        )
        results = [0.01] * periods
        df = pd.DataFrame(
            {"open": date_range_open, "close": date_range_close, "result": results}
        )
        passed = utils.challenge_pass(df)
        self.assertTrue((passed["pass"] == "not failed").all())

    def test_challenge_pass_check_one(self):
        date_range_open = pd.date_range(start="2020-1-1", freq="D", periods=32)
        date_range_close = pd.date_range(start="2020-1-1 00:05", freq="D", periods=32)
        results = [0.01] * 10 + [1.0] * 5 + [-1.0] * 6 + [0.8] * 11
        df = pd.DataFrame(
            {"open": date_range_open, "close": date_range_close, "result": results}
        )
        passed = utils.challenge_pass(df)
        self.assertEqual(len(passed), 1)
        self.assertEqual(passed.index[0], pd.Timestamp("2020-1-1 00:00"))
        self.assertEqual(passed["pass"].iloc[0], "not failed")


if __name__ == "__main__":
    unittest.main()
