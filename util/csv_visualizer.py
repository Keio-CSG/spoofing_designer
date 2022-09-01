from asyncio import sleep
import numpy as np
import open3d as o3d


class CsvVisualizer:
    """
    点群データをノンブロッキングで表示する
    """
    def __init__(self, init_data: np.ndarray):
        self.pcd = o3d.geometry.PointCloud()
        self.pcd.points = o3d.utility.Vector3dVector(init_data)
        self.pcd.colors = o3d.utility.Vector3dVector(np.full_like(init_data, 0.2))
        self.vis = None
        self.on_stop = None
        self.finished = False
        self.data_for_update = None

    def start(self, on_stop=None):
        self.on_stop = on_stop
        self.vis = o3d.visualization.VisualizerWithKeyCallback()
        self.vis.create_window()
        self.vis.register_key_callback(256, self.close_window) # ESC

        mesh = o3d.geometry.TriangleMesh.create_coordinate_frame()
        self.vis.add_geometry(self.pcd)
        self.vis.add_geometry(mesh)
        while not self.finished:
            if self.data_for_update:
                self.pcd.points = o3d.utility.Vector3dVector(self.data_for_update)
                self.pcd.colors = o3d.utility.Vector3dVector(np.full_like(self.data_for_update, 0.2))
                self.vis.update_geometry(self.pcd)
                self.data_for_update = None
            self.vis.poll_events()
            self.vis.update_renderer()

    def update_with_data(self, data):
        self.data_for_update = data

    def stop(self):
        self.vis.destroy_window()
        self.finished = True
        if self.on_stop:
            self.on_stop()

    def get_points_array(self) -> np.ndarray:
        return np.random.rand(1000, 3)

    def close_window(self, vis):
        vis.destroy_window()
        self.finished = True
        if self.on_stop:
            self.on_stop()
        return False