#!/usr/bin/env python3

"""Test for the TRACE interface

@author: Stijn Franssen-van Rijsingen, stijn.franssen@nrgpallas.com
@date: 20-12-2025
"""

# Internal packages
from pvisor import read_file, interpolate_trace, get_time_vector_axial, get_axial_profile

# External packages
from pathlib import Path

# Data handeling
import pandas as pd
import numpy as np

# Get directory so the relap files can be found
current_dir = Path(__file__).parent


def test_read_TRACE():

    filename = Path("test_input.xtv")

    df = read_file(current_dir / filename, code="TRACE")

    # df.to_csv(filename.with_suffix(".csv"))

    df_expected = pd.read_csv(
        current_dir / filename.with_suffix(".csv"),
        dtype=np.float32,
        index_col="time",
    )

    pd.testing.assert_frame_equal(df, df_expected)

    return


def test_trace_interpolation():

    filename = Path("test_input.xtv")
    path = current_dir / filename

    # Test time interpolation
    val_time = interpolate_trace(path, "pn-10A03", time=0.5)
    assert np.isclose(val_time, 100022.80746847606)

    # Test spatial and temporal interpolation
    val_axial = interpolate_trace(path, "pn-10", time=0.5, z_loc=0.05)
    assert np.isclose(val_axial, 100099.99439237456)


def test_trace_time_vector_axial():

    filename = Path("test_input.xtv")
    path = current_dir / filename

    time_vector = get_time_vector_axial(path, "pn-10", z_loc=0.05)
    assert len(time_vector) == 2
    assert np.isclose(time_vector[0][0], 0.0)
    assert np.isclose(time_vector[0][1], 100000.0)
    assert np.isclose(time_vector[1][0], 1.0147786)
    assert np.isclose(time_vector[1][1], 100202.944)


def test_trace_axial_profile():

    filename = Path("test_input.xtv")
    path = current_dir / filename

    profile = get_axial_profile(path, time=0.5, channel="pn-10")
    assert len(profile) == 6
    assert np.isclose(profile[0][0], 0.0133333335)
    assert np.isclose(profile[0][1], 100269.8479)


if __name__ == "__main__":
    test_read_TRACE()
    test_trace_interpolation()
    test_trace_time_vector_axial()
    test_trace_axial_profile()
