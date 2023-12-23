import numpy as np
import argparse
import os
import sys
import subprocess
from util.csv_points_converter import convert_to_points
from util.csv_visualizer import CsvVisualizer

from util.observer import CsvHandler
from util.load_csv_with_mask import load_csv_with_mask


def get_points_array() -> np.ndarray:
    return np.random.rand(1000, 3)


def main(path: str, no_editor: bool, distance_m: float):
    base_name = os.path.basename(path)
    dir_name = os.path.dirname(os.path.abspath(path))

    # Excelの起動
    if not no_editor:
        subprocess.Popen(["start", os.path.abspath(path)], shell=True)

    csv_visualizer = None

    def on_csv_updated(data: np.ndarray):
        data = convert_to_points(data, distance_m)
        csv_visualizer.update_with_data(data)

    csv_handler = CsvHandler([base_name], dir_name, on_csv_updated)
    init_data = load_csv_with_mask(path)
    init_data = convert_to_points(init_data, distance_m)
    csv_visualizer = CsvVisualizer(init_data)
    csv_visualizer.start(on_stop=csv_handler.stop)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to the file to watch")
    parser.add_argument("--no_editor", help="don't open editor", action="store_true")
    parser.add_argument("-d", "--distance_m", help="distance in meters", type=float, default=150)
    if len(sys.argv) == 1:
        # if no arguments, show help
        parser.print_help(sys.stdout)
        sys.exit(0)
    args = parser.parse_args()
    if args.path:
        print("Input file path: ", args.path)
    if args.no_editor:
        print("No editor")
    if args.distance_m:
        print("Distance: ", args.distance_m)

    main(args.path, args.no_editor, args.distance_m)
