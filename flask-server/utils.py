import json

import numpy as np
import pandas as pd


class NumpyEncoder(json.JSONEncoder):
    """ Custom encoder for numpy data types """
    def default(self, obj):
        print("obj", obj, type(obj))
        if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
                            np.int16, np.int32, np.int64, np.uint8,
                            np.uint16, np.uint32, np.uint64)):

            return int(obj)

        elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
            return float(obj)

        elif isinstance(obj, (np.complex_, np.complex64, np.complex128)):
            return {'real': obj.real, 'imag': obj.imag}

        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()

        elif isinstance(obj, (np.bool_)):
            return bool(obj)

        elif isinstance(obj, (np.void, np.nan)) or np.isnan(obj):
            return None

        return json.JSONEncoder.default(self, obj)


def merge_cells_and_metadata():
    metadata_df = pd.read_csv('metadata.csv')
    metadata_df.drop("uuid", axis=1, inplace=True)
    cells_df = pd.read_csv('Integrated.csv')
    cells_df.drop("time_point", axis=1, inplace=True)
    df = cells_df.merge(metadata_df, left_on='metadata', right_on='id')
    df = df.dropna(axis=1, how='all')
    print("DATA:", df.columns)
    return df
