"""
Test for the MELCOR interface

@author: Stijn Franssen-van Rijsingen, stijn.franssen@nrgpallas.com
@date: 20-12-2025
"""

# Internal packages
from pvisor import read_file

# External packages
from pathlib import Path

# Data handeling
import pandas as pd
import numpy as np

# Get directory so the relap files can be found
current_dir = Path(__file__).parent


def test_read_MELCOR():

    filename = Path("PVISOR.PTF")

    df = read_file(current_dir / filename, code="MELCOR")

    # These columns are inconsistent between identical runs
    # when performed on different hardware, so drop them.
    # df.drop(columns=["WARP", "LOCALWARP"], inplace=True)

    # For re-generating target CSV
    # df.to_csv(filename.with_suffix(".csv"))

    df_expected = pd.read_csv(
        current_dir / filename.with_suffix(".csv"),
        dtype=np.float32,
        index_col="time",
    )

    pd.testing.assert_frame_equal(df, df_expected)

    return


if __name__ == "__main__":
    test_read_MELCOR()
