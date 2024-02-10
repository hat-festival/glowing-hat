import math

import numpy as np

# import scipy


def round_up_to_even(f):  # noqa: D103
    return int(math.ceil(f / 2.0) * 2)


class numpy_data_buffer:  # noqa: N801
    """
    A fast, circular FIFO buffer in numpy with minimal memory interactions by using an array of index pointers
    """  # noqa: E501, D200, D212, D400, D415

    def __init__(  # noqa: D107, PLR0913
        self,
        n_windows,
        samples_per_window,
        dtype=np.float32,
        start_value=0,
        data_dimensions=1,
    ):
        self.n_windows = n_windows
        self.data_dimensions = data_dimensions
        self.samples_per_window = samples_per_window
        self.data = start_value * np.ones(
            (self.n_windows, self.samples_per_window), dtype=dtype
        )

        if self.data_dimensions == 1:
            self.total_samples = self.n_windows * self.samples_per_window
        else:
            self.total_samples = self.n_windows

        self.elements_in_buffer = 0
        self.overwrite_index = 0

        self.indices = np.arange(self.n_windows, dtype=np.int32)
        self.last_window_id = np.max(self.indices)
        self.index_order = np.argsort(self.indices)

    def append_data(self, data_window):  # noqa: D102
        self.data[self.overwrite_index, :] = data_window

        self.last_window_id += 1
        self.indices[self.overwrite_index] = self.last_window_id
        self.index_order = np.argsort(self.indices)

        self.overwrite_index += 1
        self.overwrite_index = self.overwrite_index % self.n_windows

        self.elements_in_buffer += 1
        self.elements_in_buffer = min(self.n_windows, self.elements_in_buffer)

    def get_most_recent(self, window_size):  # noqa: D102
        ordered_dataframe = self.data[self.index_order]
        if self.data_dimensions == 1:
            ordered_dataframe = np.hstack(ordered_dataframe)
        return ordered_dataframe[self.total_samples - window_size :]

    def get_buffer_data(self):  # noqa: D102
        return self.data[: self.elements_in_buffer]
