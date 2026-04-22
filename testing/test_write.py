import unittest

import pandas as pd

from src.write import _build_chapter_interpretations


class TestBuildChapterInterpretations(unittest.TestCase):
    def test_uses_existing_interpretation_column(self):
        df = pd.DataFrame(
            {
                "chapter": ["A", "A", "B"],
                "interpretation": ["Alpha summary", "", "Beta summary"],
                "value": [10, 20, 5],
            }
        )

        result = _build_chapter_interpretations(
            data=df,
            chapter_column="chapter",
            interpretation_column="interpretation",
        )

        expected = pd.DataFrame(
            {
                "chapter": ["A", "B"],
                "interpretation": ["Alpha summary", "Beta summary"],
            }
        )
        pd.testing.assert_frame_equal(
            result.reset_index(drop=True),
            expected.reset_index(drop=True),
        )

    def test_generates_fallback_interpretation(self):
        df = pd.DataFrame(
            {
                "chapter": ["A", "A", "B"],
                "metric_1": [10, 20, 30],
                "metric_2": [2, 4, 8],
            }
        )

        result = _build_chapter_interpretations(
            data=df,
            chapter_column="chapter",
            interpretation_column=None,
        )

        self.assertListEqual(result["chapter"].tolist(), ["A", "B"])
        self.assertIn("Rows: 2", result.loc[0, "interpretation"])
        self.assertIn("metric_1 avg: 15.00", result.loc[0, "interpretation"])
        self.assertIn("metric_2 avg: 3.00", result.loc[0, "interpretation"])
        self.assertEqual(result.loc[1, "chapter"], "B")
        self.assertIn("Rows: 1", result.loc[1, "interpretation"])
        self.assertIn("metric_1 avg: 30.00", result.loc[1, "interpretation"])
        self.assertIn("metric_2 avg: 8.00", result.loc[1, "interpretation"])


if __name__ == "__main__":
    unittest.main()
