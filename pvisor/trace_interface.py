"""
Contains the code for reading TRACE XTV files.

The keyword for the TRACE interface for using in the ``pvisor.read_file()`` function is: ``TRACE``.

Reads in a binary TRACE XTV file and returns it in a pandas dataframe using the ``xtvreader`` library.
It also provides helper functions for spatial and temporal interpolation.
"""

import pandas as pd
from pathlib import Path
from typing import Union, List, Tuple
import xtvreader

def _read_trace(path: Union[str, Path]) -> pd.DataFrame:
    """
    Reads in a TRACE XTV file and returns it in a pandas DataFrame.

    Parameters
    ----------
    path: str or Path
        The path to the TRACE XTV file to read.

    Returns
    -------
    df: pd.DataFrame
        The data in a pandas DataFrame, indexed by time.
    """
    if isinstance(path, str):
        path = Path(path)
        
    with open(path, "rb") as f:
        xtv = xtvreader.XtvFile(f)
        
        # Get all variables and filter to only time-dependent (dynamic) ones
        xtv_dict = xtv.getList(list_all=True)
        variables = []
        for (id, comp_type), c_obj in xtv.components.items():
            comp_key_type = "htstr" if comp_type == "htstrc" else comp_type
            comp_key = f"{comp_key_type}-{id}"
            if comp_key not in xtv_dict:
                continue
            td_channels = {name for name, chan in c_obj.channels.items() if chan.freqAt.strip() == "TD"}
            for gen_name in xtv_dict[comp_key]:
                for base_name in td_channels:
                    if gen_name == base_name or gen_name.startswith(base_name + "-") or gen_name.startswith(base_name + "A") or gen_name.startswith(base_name + "R") or gen_name.startswith(base_name + "T"):
                        variables.append(gen_name)
                        break
            
        # Bulk load variable data
        data_dict = {}
        for var in variables:
            try:
                vector = xtv.getTimeVector(var)
                data_dict[var] = [val for _, val in vector]
            except Exception:
                # Skip any problematic channels
                continue
                
        df = pd.DataFrame(data_dict, index=xtv.times, dtype="float32")
        df.index = df.index.astype("float32")
        df.index.name = "time"
        return df

def interpolate_trace(path: Union[str, Path], channel: str, time: float, z_loc: float = None) -> float:
    """
    Interpolate a TRACE XTV variable at a specific time and optional axial coordinate.
    
    If z_loc is provided, performs spatial interpolation along the axial coordinate.
    If the time is between edits, performs linear time interpolation.
    """
    if isinstance(path, str):
        path = Path(path)
        
    with open(path, "rb") as f:
        xtv = xtvreader.XtvFile(f)
        if z_loc is not None:
            return xtv.getAxialDataChannel(time, channel, z_loc)
        else:
            return xtv.getDataChannel(time, channel)

def get_time_vector_axial(path: Union[str, Path], channel: str, z_loc: float) -> List[Tuple[float, float]]:
    """
    Retrieve a list of (time, value) pairs for a data channel interpolated at a specific axial location.
    """
    if isinstance(path, str):
        path = Path(path)
        
    with open(path, "rb") as f:
        xtv = xtvreader.XtvFile(f)
        return xtv.getTimeVectorAxial(channel, z_loc)

def get_axial_profile(path: Union[str, Path], time: float, channel: str) -> List[Tuple[float, float]]:
    """
    Retrieve a list of (axial_coordinate, value) pairs for a data channel at a specific time.
    """
    if isinstance(path, str):
        path = Path(path)
        
    with open(path, "rb") as f:
        xtv = xtvreader.XtvFile(f)
        return xtv.getAxialVector(time, channel)
