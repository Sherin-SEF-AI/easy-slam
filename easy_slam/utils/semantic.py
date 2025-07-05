import numpy as np
try:
    from ultralytics import YOLO
except ImportError:
    YOLO = None

class SemanticMapper:
    """
    Semantic mapping using YOLOv8 for object detection.
    """
    def __init__(self, model_path='yolov8n.pt'):
        if YOLO is None:
            raise ImportError("ultralytics package not installed. Run 'pip install ultralytics'.")
        self.model = YOLO(model_path)

    def detect(self, rgb):
        """
        Run object detection on an RGB image.
        Args:
            rgb: RGB image (numpy array)
        Returns:
            List of detections: [{class, conf, bbox}]
        """
        results = self.model(rgb)
        detections = []
        for r in results:
            for box in r.boxes:
                detections.append({
                    'class': int(box.cls[0]),
                    'conf': float(box.conf[0]),
                    'bbox': box.xyxy[0].tolist()
                })
        return detections

    def attach_semantics(self, pcd, rgb, depth, intrinsic):
        """
        Attach semantic labels to 3D points in a point cloud.
        Args:
            pcd: Open3D PointCloud
            rgb: RGB image
            depth: Depth image
            intrinsic: Open3D camera intrinsic
        Returns:
            List of (point, label) tuples
        """
        detections = self.detect(rgb)
        points = np.asarray(pcd.points)
        labels = np.full(len(points), -1, dtype=int)
        # Project 3D points to 2D
        fx, fy = intrinsic.get_focal_length()
        cx, cy = intrinsic.get_principal_point()
        for i, pt in enumerate(points):
            x, y, z = pt
            if z <= 0: continue
            u = int(fx * x / z + cx)
            v = int(fy * y / z + cy)
            for det in detections:
                x1, y1, x2, y2 = det['bbox']
                if x1 <= u <= x2 and y1 <= v <= y2:
                    labels[i] = det['class']
                    break
        return list(zip(points, labels)) 