from lib.sorters.axis_manager import AxisManager


def load_sorts():
    """Load the sorts into Redis if required."""
    axis_manager = AxisManager(cube_radius=1.1)
    axis_manager.populate()


if __name__ == "__main__":
    load_sorts()
