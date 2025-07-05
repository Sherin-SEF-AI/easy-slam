import sys
import threading
import time
import psutil
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QPushButton, 
                             QComboBox, QCheckBox, QTextEdit, QVBoxLayout, QHBoxLayout, 
                             QFileDialog, QProgressBar, QGroupBox, QGridLayout, QTabWidget,
                             QSplitter, QFrame, QSlider, QSpinBox, QDoubleSpinBox, QMenuBar,
                             QMenu, QMessageBox, QInputDialog)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt6.QtGui import QPixmap, QImage, QPalette, QColor, QFont, QPainter, QPen, QAction
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D

class SLAMThread(QThread):
    """Thread for running SLAM in background"""
    frame_ready = pyqtSignal(np.ndarray)
    log_ready = pyqtSignal(str)
    status_ready = pyqtSignal(str)
    trajectory_ready = pyqtSignal(list)
    map_ready = pyqtSignal(object)
    features_ready = pyqtSignal(list)
    performance_ready = pyqtSignal(dict)
    
    def __init__(self, slam_config):
        super().__init__()
        self.slam_config = slam_config
        self.running = False
        self.slam = None
        self.frame_count = 0
        self.start_time = time.time()
        
    def run(self):
        try:
            from easy_slam import EasySLAM
            
            self.log_ready.emit("[GUI] Creating EasySLAM instance...")
            
            # Initialize SLAM
            self.slam = EasySLAM(
                camera=self.slam_config['camera'],
                algorithm=self.slam_config['algorithm'],
                visualization=False,  # We'll handle visualization in GUI
                save_trajectory=self.slam_config['save_trajectory'],
                output_dir="./results"
            )
            
            self.running = True
            self.log_ready.emit("[GUI] SLAM initialized successfully")
            
            # Don't call slam.start() - we'll handle the processing loop ourselves
            # self.slam.start()  # This was causing the immediate stop
            
            # Main processing loop
            while self.running:
                try:
                    # Get frame from sensor
                    if hasattr(self.slam, 'sensor') and self.slam.sensor:
                        frame = self.slam.sensor.read()
                        if frame is not None:
                            # Convert BGR to RGB for Qt
                            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            
                            # Emit frame for GUI display
                            self.frame_ready.emit(frame_rgb)
                            
                            # Process with SLAM
                            if hasattr(self.slam, 'slam_algorithm') and self.slam.slam_algorithm:
                                result = self.slam.slam_algorithm.process(frame)
                                
                                if result and hasattr(result, 'pose') and result.pose is not None:
                                    self.slam.trajectory.append(result.pose)
                                    
                                    # Emit trajectory updates
                                    if len(self.slam.trajectory) % 5 == 0:
                                        self.trajectory_ready.emit(self.slam.trajectory)
                                
                                # Emit feature points if available
                                if hasattr(result, 'features') and result.features is not None:
                                    self.features_ready.emit(result.features)
                                
                                # Emit map data if available
                                if hasattr(result, 'map') and result.map is not None:
                                    self.map_ready.emit(result.map)
                            
                            self.frame_count += 1
                            
                            # Update performance metrics every 30 frames
                            if self.frame_count % 30 == 0:
                                try:
                                    fps = self.frame_count / (time.time() - self.start_time)
                                    memory_mb = psutil.Process().memory_info().rss / 1024 / 1024
                                    cpu_percent = psutil.Process().cpu_percent()
                                    
                                    performance_data = {
                                        'fps': fps,
                                        'frames': self.frame_count,
                                        'memory_mb': memory_mb,
                                        'cpu_percent': cpu_percent
                                    }
                                    self.performance_ready.emit(performance_data)
                                    
                                    status = f"FPS: {fps:.1f}, Frames: {self.frame_count}"
                                    self.status_ready.emit(status)
                                    self.log_ready.emit(f"[GUI] {status}")
                                except Exception as perf_error:
                                    self.log_ready.emit(f"[WARNING] Performance monitoring error: {perf_error}")
                        else:
                            self.log_ready.emit("[WARNING] No frame received from sensor")
                            
                except Exception as e:
                    self.log_ready.emit(f"[ERROR] Frame processing: {e}")
                    import traceback
                    self.log_ready.emit(f"[ERROR] Traceback: {traceback.format_exc()}")
                    break
                    
                time.sleep(0.01)  # Small delay to prevent overwhelming
                
        except Exception as e:
            self.log_ready.emit(f"[ERROR] SLAM initialization: {e}")
            import traceback
            self.log_ready.emit(f"[ERROR] Initialization traceback: {traceback.format_exc()}")
            
    def stop(self):
        self.running = False
        if self.slam:
            # Don't call slam.stop() as it releases the camera
            # self.slam.stop()  # This was causing camera release
            pass
        self.log_ready.emit("[GUI] SLAM stopped")

class TrajectoryPlot(FigureCanvas):
    """Enhanced Matplotlib widget for trajectory visualization"""
    def __init__(self, parent=None, width=8, height=6, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor='#2b2b2b')
        self.axes = self.fig.add_subplot(111, facecolor='#2b2b2b')
        super().__init__(self.fig)
        self.setParent(parent)
        self._init_plot()
        self.trajectory_data = []
        
    def _init_plot(self):
        self.axes.set_xlabel('X (m)', color='white', fontsize=10)
        self.axes.set_ylabel('Y (m)', color='white', fontsize=10)
        self.axes.set_title('SLAM Trajectory', color='white', fontsize=12, fontweight='bold')
        self.axes.grid(True, alpha=0.3, color='gray')
        self.axes.tick_params(colors='white')
        self.fig.tight_layout()
        
    def update_trajectory(self, trajectory):
        if trajectory and len(trajectory) > 1:
            try:
                self.axes.clear()
                self._init_plot()
                
                # Extract x, y coordinates
                x_coords = []
                y_coords = []
                for pose in trajectory:
                    if isinstance(pose, (list, tuple)) and len(pose) >= 2:
                        try:
                            x_coords.append(float(pose[0]))
                            y_coords.append(float(pose[1]))
                        except (ValueError, TypeError):
                            continue
                
                if len(x_coords) > 1:
                    # Plot trajectory with gradient color
                    colors = plt.cm.viridis(np.linspace(0, 1, len(x_coords)))
                    for i in range(len(x_coords)-1):
                        self.axes.plot(x_coords[i:i+2], y_coords[i:i+2], 
                                     color=colors[i], linewidth=2, alpha=0.8)
                    
                    # Mark start and end points
                    self.axes.scatter(x_coords[0], y_coords[0], c='green', s=100, 
                                    marker='o', label='Start', zorder=5)
                    self.axes.scatter(x_coords[-1], y_coords[-1], c='red', s=100, 
                                    marker='*', label='Current', zorder=5)
                    
                    # Add legend
                    self.axes.legend(loc='upper right')
                    
                    # Auto-scale to fit trajectory
                    self.axes.set_aspect('equal', adjustable='box')
                
                self.draw()
            except Exception as e:
                print(f"Trajectory plot error: {e}")

class Map3DPlot(FigureCanvas):
    """3D map visualization"""
    def __init__(self, parent=None, width=8, height=6, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor='#2b2b2b')
        self.axes = self.fig.add_subplot(111, projection='3d', facecolor='#2b2b2b')
        super().__init__(self.fig)
        self.setParent(parent)
        self._init_plot()
        
    def _init_plot(self):
        self.axes.set_xlabel('X (m)', color='white')
        self.axes.set_ylabel('Y (m)', color='white')
        self.axes.set_zlabel('Z (m)', color='white')
        self.axes.set_title('3D Map View', color='white', fontsize=12, fontweight='bold')
        self.axes.tick_params(colors='white')
        
    def update_map(self, map_data):
        if map_data is not None:
            self.axes.clear()
            self._init_plot()
            
            # Generate sample 3D points for demonstration
            x = np.random.randn(100) * 2
            y = np.random.randn(100) * 2
            z = np.random.randn(100) * 0.5
            
            self.axes.scatter(x, y, z, c='cyan', alpha=0.6, s=20)
            self.draw()

class PerformanceWidget(QWidget):
    """Enhanced widget for performance monitoring"""
    def __init__(self):
        super().__init__()
        self._init_ui()
        
    def _init_ui(self):
        layout = QVBoxLayout(self)
        
        # Performance metrics with better styling
        metrics_group = QGroupBox("Real-time Metrics")
        metrics_layout = QGridLayout(metrics_group)
        
        # FPS
        self.fps_label = QLabel('FPS: 0.0')
        self.fps_label.setStyleSheet('color: #00ff00; font-size: 16px; font-weight: bold; padding: 10px; background: #1a1a1a; border-radius: 5px;')
        
        # Frames
        self.frames_label = QLabel('Frames: 0')
        self.frames_label.setStyleSheet('color: #00ffff; font-size: 16px; font-weight: bold; padding: 10px; background: #1a1a1a; border-radius: 5px;')
        
        # Memory
        self.memory_label = QLabel('Memory: 0 MB')
        self.memory_label.setStyleSheet('color: #ffff00; font-size: 16px; font-weight: bold; padding: 10px; background: #1a1a1a; border-radius: 5px;')
        
        # CPU
        self.cpu_label = QLabel('CPU: 0%')
        self.cpu_label.setStyleSheet('color: #ff6b6b; font-size: 16px; font-weight: bold; padding: 10px; background: #1a1a1a; border-radius: 5px;')
        
        # Progress bars
        self.fps_bar = QProgressBar()
        self.fps_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #404040;
                border-radius: 5px;
                text-align: center;
                background-color: #1a1a1a;
            }
            QProgressBar::chunk {
                background-color: #00ff00;
                border-radius: 3px;
            }
        """)
        self.fps_bar.setMaximum(60)
        
        self.memory_bar = QProgressBar()
        self.memory_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #404040;
                border-radius: 5px;
                text-align: center;
                background-color: #1a1a1a;
            }
            QProgressBar::chunk {
                background-color: #ffff00;
                border-radius: 3px;
            }
        """)
        self.memory_bar.setMaximum(1000)
        
        # Layout
        metrics_layout.addWidget(self.fps_label, 0, 0)
        metrics_layout.addWidget(self.frames_label, 0, 1)
        metrics_layout.addWidget(self.memory_label, 1, 0)
        metrics_layout.addWidget(self.cpu_label, 1, 1)
        metrics_layout.addWidget(QLabel('FPS Progress:'), 2, 0)
        metrics_layout.addWidget(self.fps_bar, 2, 1)
        metrics_layout.addWidget(QLabel('Memory Progress:'), 3, 0)
        metrics_layout.addWidget(self.memory_bar, 3, 1)
        
        layout.addWidget(metrics_group)
        
        # System info
        system_group = QGroupBox("System Information")
        system_layout = QVBoxLayout(system_group)
        
        self.system_info = QTextEdit()
        self.system_info.setReadOnly(True)
        self.system_info.setMaximumHeight(100)
        self.system_info.setStyleSheet('QTextEdit { background-color: #1a1a1a; color: #ffffff; border: 1px solid #404040; }')
        
        # Get system info
        cpu_count = psutil.cpu_count()
        memory = psutil.virtual_memory()
        system_text = f"CPU Cores: {cpu_count}\n"
        system_text += f"Total Memory: {memory.total / 1024 / 1024 / 1024:.1f} GB\n"
        system_text += f"Available Memory: {memory.available / 1024 / 1024 / 1024:.1f} GB"
        
        self.system_info.setText(system_text)
        system_layout.addWidget(self.system_info)
        
        layout.addWidget(system_group)
        
    def update_metrics(self, performance_data):
        fps = performance_data.get('fps', 0)
        frames = performance_data.get('frames', 0)
        memory_mb = performance_data.get('memory_mb', 0)
        cpu_percent = performance_data.get('cpu_percent', 0)
        
        self.fps_label.setText(f'FPS: {fps:.1f}')
        self.frames_label.setText(f'Frames: {frames}')
        self.memory_label.setText(f'Memory: {memory_mb:.1f} MB')
        self.cpu_label.setText(f'CPU: {cpu_percent:.1f}%')
        
        # Update progress bars
        self.fps_bar.setValue(min(int(fps), 60))
        self.memory_bar.setValue(min(int(memory_mb), 1000))

class FeatureVisualization(QWidget):
    """Widget for feature point visualization"""
    def __init__(self):
        super().__init__()
        self._init_ui()
        
    def _init_ui(self):
        layout = QVBoxLayout(self)
        
        # Feature plot
        self.feature_fig = Figure(figsize=(8, 6), facecolor='#2b2b2b')
        self.feature_axes = self.feature_fig.add_subplot(111, facecolor='#2b2b2b')
        self.feature_canvas = FigureCanvas(self.feature_fig)
        
        self.feature_axes.set_title('Feature Points', color='white', fontsize=12)
        self.feature_axes.set_xlabel('X', color='white')
        self.feature_axes.set_ylabel('Y', color='white')
        self.feature_axes.tick_params(colors='white')
        self.feature_axes.grid(True, alpha=0.3, color='gray')
        
        layout.addWidget(self.feature_canvas)
        
    def update_features(self, features):
        if features:
            self.feature_axes.clear()
            self.feature_axes.set_title('Feature Points', color='white', fontsize=12)
            self.feature_axes.set_xlabel('X', color='white')
            self.feature_axes.set_ylabel('Y', color='white')
            self.feature_axes.tick_params(colors='white')
            self.feature_axes.grid(True, alpha=0.3, color='gray')
            
            # Plot feature points
            x_coords = [f[0] for f in features if len(f) >= 2]
            y_coords = [f[1] for f in features if len(f) >= 2]
            
            if x_coords and y_coords:
                self.feature_axes.scatter(x_coords, y_coords, c='red', s=20, alpha=0.7)
            
            self.feature_canvas.draw()

class EasySLAMMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        try:
            print("[GUI] Initializing EasySLAM Main Window...")
            self.setWindowTitle('Easy-SLAM GUI - Advanced Visualization & Analysis')
            self.setGeometry(100, 100, 1600, 1000)
            self.slam_thread = None
            
            print("[GUI] Initializing UI...")
            self._init_ui()
            print("[GUI] Connecting signals...")
            self._connect_signals()
            print("[GUI] Applying dark theme...")
            self._apply_dark_theme()
            print("[GUI] Creating menu...")
            self._create_menu()
            
            # Add initial log message
            self.log_text.append("[GUI] Easy-SLAM GUI initialized with advanced visualizations and analysis tools")
            print("[GUI] Main window initialization complete")
        except Exception as e:
            print(f"[ERROR] Failed to initialize main window: {e}")
            import traceback
            print(f"[ERROR] Traceback: {traceback.format_exc()}")
            raise
        
    def _create_menu(self):
        """Create menu bar with additional functions"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        save_action = QAction('Save Results', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_results)
        file_menu.addAction(save_action)
        
        load_action = QAction('Load Session', self)
        load_action.setShortcut('Ctrl+O')
        load_action.triggered.connect(self.load_session)
        file_menu.addAction(load_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Tools menu
        tools_menu = menubar.addMenu('Tools')
        
        calibrate_action = QAction('Camera Calibration', self)
        calibrate_action.triggered.connect(self.calibrate_camera)
        tools_menu.addAction(calibrate_action)
        
        settings_action = QAction('Settings', self)
        settings_action.triggered.connect(self.show_settings)
        tools_menu.addAction(settings_action)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def _apply_dark_theme(self):
        """Apply modern dark theme"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QMenuBar {
                background-color: #2d2d2d;
                color: #ffffff;
                border-bottom: 1px solid #404040;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 5px 10px;
            }
            QMenuBar::item:selected {
                background-color: #404040;
            }
            QMenu {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #404040;
            }
            QMenu::item:selected {
                background-color: #404040;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #404040;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
                background-color: #2d2d2d;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #ffffff;
            }
            QPushButton {
                background-color: #404040;
                border: 1px solid #606060;
                border-radius: 3px;
                padding: 5px;
                color: #ffffff;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #505050;
            }
            QPushButton:pressed {
                background-color: #303030;
            }
            QPushButton:disabled {
                background-color: #2a2a2a;
                color: #666666;
            }
            QComboBox {
                background-color: #404040;
                border: 1px solid #606060;
                border-radius: 3px;
                padding: 5px;
                color: #ffffff;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #ffffff;
            }
            QCheckBox {
                color: #ffffff;
                spacing: 5px;
            }
            QCheckBox::indicator {
                width: 15px;
                height: 15px;
            }
            QCheckBox::indicator:unchecked {
                border: 1px solid #606060;
                background-color: #404040;
            }
            QCheckBox::indicator:checked {
                border: 1px solid #606060;
                background-color: #4CAF50;
            }
            QTextEdit {
                background-color: #1a1a1a;
                border: 1px solid #404040;
                border-radius: 3px;
                color: #00ff00;
                font-family: 'Courier New', monospace;
                font-size: 11px;
            }
            QLabel {
                color: #ffffff;
            }
            QTabWidget::pane {
                border: 1px solid #404040;
                background-color: #2d2d2d;
            }
            QTabBar::tab {
                background-color: #404040;
                color: #ffffff;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #505050;
            }
        """)
        
    def _init_ui(self):
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        
        # Control Panel
        control_group = QGroupBox("SLAM Controls")
        control_layout = QGridLayout(control_group)
        
        # Camera selection
        control_layout.addWidget(QLabel('Camera:'), 0, 0)
        self.camera_combo = QComboBox()
        self.camera_combo.addItems(['0 (Webcam)', 'realsense', 'stereo', 'lidar', 'Dataset...'])
        control_layout.addWidget(self.camera_combo, 0, 1)
        
        # Algorithm selection
        control_layout.addWidget(QLabel('Algorithm:'), 0, 2)
        self.alg_combo = QComboBox()
        self.alg_combo.addItems(['orb_slam', 'fastslam', 'graphslam', 'visual_inertial', 'rgbd_slam'])
        control_layout.addWidget(self.alg_combo, 0, 3)
        
        # Advanced features
        self.semantic_cb = QCheckBox('Semantic Mapping')
        self.fusion_cb = QCheckBox('Sensor Fusion')
        self.merging_cb = QCheckBox('Map Merging')
        self.profiling_cb = QCheckBox('Profiling')
        self.save_trajectory_cb = QCheckBox('Save Trajectory')
        self.save_trajectory_cb.setChecked(True)
        
        control_layout.addWidget(self.semantic_cb, 1, 0)
        control_layout.addWidget(self.fusion_cb, 1, 1)
        control_layout.addWidget(self.merging_cb, 1, 2)
        control_layout.addWidget(self.profiling_cb, 1, 3)
        control_layout.addWidget(self.save_trajectory_cb, 1, 4)
        
        # Start/Stop buttons
        self.start_btn = QPushButton('Start SLAM')
        self.start_btn.setStyleSheet('QPushButton { background-color: #4CAF50; color: white; font-weight: bold; }')
        self.stop_btn = QPushButton('Stop SLAM')
        self.stop_btn.setStyleSheet('QPushButton { background-color: #f44336; color: white; font-weight: bold; }')
        self.stop_btn.setEnabled(False)
        
        control_layout.addWidget(self.start_btn, 2, 0, 1, 2)
        control_layout.addWidget(self.stop_btn, 2, 2, 1, 2)
        
        # Status bar
        self.status_label = QLabel('Ready')
        self.status_label.setStyleSheet('QLabel { background-color: #404040; padding: 5px; border: 1px solid #606060; border-radius: 3px; }')
        control_layout.addWidget(self.status_label, 2, 4)
        
        main_layout.addWidget(control_group)
        
        # Create tab widget for different views
        self.tab_widget = QTabWidget()
        
        # Video tab
        video_widget = QWidget()
        video_layout = QVBoxLayout(video_widget)
        
        self.video_label = QLabel('Click "Start SLAM" to begin')
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setStyleSheet('background: #1a1a1a; color: #ffffff; font-size: 16px; border: 2px solid #404040; border-radius: 5px;')
        self.video_label.setFixedHeight(400)
        video_layout.addWidget(self.video_label)
        
        self.tab_widget.addTab(video_widget, "Live Video")
        
        # Trajectory tab
        trajectory_widget = QWidget()
        trajectory_layout = QVBoxLayout(trajectory_widget)
        
        self.trajectory_plot = TrajectoryPlot(trajectory_widget, width=10, height=7)
        trajectory_layout.addWidget(self.trajectory_plot)
        
        self.tab_widget.addTab(trajectory_widget, "2D Trajectory")
        
        # 3D Map tab
        map3d_widget = QWidget()
        map3d_layout = QVBoxLayout(map3d_widget)
        
        self.map3d_plot = Map3DPlot(map3d_widget, width=10, height=7)
        map3d_layout.addWidget(self.map3d_plot)
        
        self.tab_widget.addTab(map3d_widget, "3D Map")
        
        # Features tab
        features_widget = QWidget()
        features_layout = QVBoxLayout(features_widget)
        
        self.feature_viz = FeatureVisualization()
        features_layout.addWidget(self.feature_viz)
        
        self.tab_widget.addTab(features_widget, "Feature Points")
        
        # Performance tab
        performance_widget = QWidget()
        performance_layout = QVBoxLayout(performance_widget)
        
        self.performance_widget = PerformanceWidget()
        performance_layout.addWidget(self.performance_widget)
        
        self.tab_widget.addTab(performance_widget, "Performance")
        
        main_layout.addWidget(self.tab_widget)
        
        # Log output
        log_group = QGroupBox("Log Output")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFixedHeight(150)
        log_layout.addWidget(self.log_text)
        
        main_layout.addWidget(log_group)
        
    def _connect_signals(self):
        """Connect UI signals to slots"""
        self.start_btn.clicked.connect(self.start_slam)
        self.stop_btn.clicked.connect(self.stop_slam)
        self.camera_combo.currentTextChanged.connect(self.on_camera_changed)
        
    def on_camera_changed(self, text):
        """Handle camera selection change"""
        if 'Dataset' in text:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Select Dataset", "", "All Files (*)"
            )
            if file_path:
                self.camera_combo.setCurrentText(file_path)
                
    def start_slam(self):
        """Start SLAM processing"""
        try:
            # Get configuration from UI
            camera_text = self.camera_combo.currentText()
            if camera_text == '0 (Webcam)':
                camera = 0
            elif camera_text == 'Dataset...':
                camera = 0  # Default to webcam
            else:
                camera = camera_text
                
            algorithm = self.alg_combo.currentText()
            
            slam_config = {
                'camera': camera,
                'algorithm': algorithm,
                'enable_semantic': self.semantic_cb.isChecked(),
                'enable_sensor_fusion': self.fusion_cb.isChecked(),
                'enable_map_merging': self.merging_cb.isChecked(),
                'enable_profiling': self.profiling_cb.isChecked(),
                'save_trajectory': self.save_trajectory_cb.isChecked()
            }
            
            self.log_text.append(f"[GUI] Initializing SLAM with {algorithm} algorithm...")
            
            # Create and start SLAM thread
            self.slam_thread = SLAMThread(slam_config)
            self.slam_thread.frame_ready.connect(self.update_video)
            self.slam_thread.log_ready.connect(self.update_log)
            self.slam_thread.status_ready.connect(self.update_status)
            self.slam_thread.trajectory_ready.connect(self.update_trajectory)
            self.slam_thread.performance_ready.connect(self.update_performance)
            self.slam_thread.features_ready.connect(self.update_features)
            
            # Connect finished signal to handle thread completion
            self.slam_thread.finished.connect(self.on_slam_finished)
            
            self.slam_thread.start()
            
            # Update UI
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.status_label.setText('SLAM Running')
            self.log_text.append(f"[GUI] SLAM thread started successfully")
            
        except Exception as e:
            self.log_text.append(f"[ERROR] Failed to start SLAM: {e}")
            import traceback
            self.log_text.append(f"[ERROR] Start SLAM traceback: {traceback.format_exc()}")
            
    def on_slam_finished(self):
        """Handle SLAM thread completion"""
        self.log_text.append("[GUI] SLAM thread finished")
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status_label.setText('Ready')
            
    def stop_slam(self):
        """Stop SLAM processing"""
        if self.slam_thread:
            self.slam_thread.stop()
            self.slam_thread.wait()
            self.slam_thread = None
            
        # Update UI
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status_label.setText('Ready')
        self.log_text.append("[GUI] SLAM stopped")
        
    def update_video(self, frame):
        """Update video display with new frame"""
        try:
            # Convert frame to QPixmap
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            
            # Scale to fit video label
            scaled_pixmap = pixmap.scaled(
                self.video_label.width(), 
                self.video_label.height(),
                Qt.AspectRatioMode.KeepAspectRatio
            )
            
            self.video_label.setPixmap(scaled_pixmap)
            
        except Exception as e:
            self.log_text.append(f"[ERROR] Video update: {e}")
            
    def update_trajectory(self, trajectory):
        """Update trajectory visualization"""
        try:
            # Convert trajectory data to proper format
            if trajectory:
                # Handle different pose formats
                processed_trajectory = []
                for i, pose in enumerate(trajectory):
                    try:
                        if isinstance(pose, np.ndarray):
                            # Handle numpy arrays (4x4 transformation matrices)
                            if pose.shape == (4, 4):
                                # Extract translation from 4x4 transformation matrix
                                x = float(pose[0, 3])  # Translation in X
                                y = float(pose[1, 3])  # Translation in Y
                                processed_trajectory.append([x, y])
                            elif pose.shape == (3, 3):
                                # 3x3 rotation matrix, assume no translation
                                processed_trajectory.append([0.0, 0.0])
                            elif len(pose) >= 2:
                                # 1D array with at least 2 elements
                                x = float(pose[0])
                                y = float(pose[1])
                                processed_trajectory.append([x, y])
                            else:
                                # Single value or invalid shape
                                continue
                        elif isinstance(pose, (list, tuple)):
                            if len(pose) >= 2:
                                x = float(pose[0]) if hasattr(pose[0], '__float__') else 0.0
                                y = float(pose[1]) if hasattr(pose[1], '__float__') else 0.0
                                processed_trajectory.append([x, y])
                        elif hasattr(pose, '__len__') and len(pose) >= 2:
                            x = float(pose[0]) if hasattr(pose[0], '__float__') else 0.0
                            y = float(pose[1]) if hasattr(pose[1], '__float__') else 0.0
                            processed_trajectory.append([x, y])
                        elif hasattr(pose, 'item'):  # numpy scalar
                            # If pose is a single value, use it as x, y=0
                            x = float(pose.item()) if hasattr(pose, 'item') else 0.0
                            processed_trajectory.append([x, 0.0])
                        else:
                            # Skip invalid poses
                            continue
                    except (ValueError, TypeError, AttributeError) as pose_error:
                        # Log the first few pose errors for debugging
                        if i < 3:
                            self.log_text.append(f"[DEBUG] Pose {i} error: {pose_error}, type: {type(pose)}")
                        continue
                
                if processed_trajectory:
                    self.trajectory_plot.update_trajectory(processed_trajectory)
        except Exception as e:
            self.log_text.append(f"[ERROR] Trajectory update: {e}")
            import traceback
            self.log_text.append(f"[ERROR] Trajectory traceback: {traceback.format_exc()}")
            
    def update_performance(self, performance_data):
        """Update performance metrics"""
        try:
            self.performance_widget.update_metrics(performance_data)
        except Exception as e:
            self.log_text.append(f"[ERROR] Performance update: {e}")
            
    def update_features(self, features):
        """Update feature visualization"""
        try:
            # Convert cv2.KeyPoint objects to coordinates
            if features and hasattr(features[0], 'pt'):
                # Extract coordinates from KeyPoint objects
                feature_coords = [(kp.pt[0], kp.pt[1]) for kp in features if hasattr(kp, 'pt')]
                self.feature_viz.update_features(feature_coords)
            elif features and isinstance(features[0], (list, tuple)):
                # Features are already coordinate pairs
                self.feature_viz.update_features(features)
            else:
                # Skip if features are in unknown format
                pass
        except Exception as e:
            self.log_text.append(f"[ERROR] Feature update: {e}")
            
    def update_log(self, message):
        """Update log display"""
        self.log_text.append(message)
        # Auto-scroll to bottom
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )
        
    def update_status(self, status):
        """Update status display"""
        self.status_label.setText(status)
        
    def save_results(self):
        """Save current results"""
        try:
            filename, _ = QFileDialog.getSaveFileName(
                self, "Save Results", "", "Text Files (*.txt);;All Files (*)"
            )
            if filename:
                with open(filename, 'w') as f:
                    f.write("Easy-SLAM Results\n")
                    f.write("=" * 50 + "\n")
                    f.write(f"Algorithm: {self.alg_combo.currentText()}\n")
                    f.write(f"Camera: {self.camera_combo.currentText()}\n")
                    f.write(f"Frames processed: {self.slam_thread.frame_count if self.slam_thread else 0}\n")
                self.log_text.append(f"[GUI] Results saved to {filename}")
        except Exception as e:
            self.log_text.append(f"[ERROR] Failed to save results: {e}")
            
    def load_session(self):
        """Load a previous session"""
        try:
            filename, _ = QFileDialog.getOpenFileName(
                self, "Load Session", "", "Text Files (*.txt);;All Files (*)"
            )
            if filename:
                self.log_text.append(f"[GUI] Loading session from {filename}")
        except Exception as e:
            self.log_text.append(f"[ERROR] Failed to load session: {e}")
            
    def calibrate_camera(self):
        """Open camera calibration tool"""
        QMessageBox.information(self, "Camera Calibration", 
                              "Camera calibration tool will be implemented in future versions.")
        
    def show_settings(self):
        """Show settings dialog"""
        QMessageBox.information(self, "Settings", 
                              "Settings dialog will be implemented in future versions.")
        
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, "About Easy-SLAM", 
                         "Easy-SLAM GUI v1.0\n\n"
                         "Advanced SLAM visualization and analysis tool\n"
                         "Built with PyQt6 and matplotlib")
        
    def closeEvent(self, event):
        """Handle window close event"""
        if self.slam_thread:
            self.stop_slam()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EasySLAMMainWindow()
    window.show()
    sys.exit(app.exec()) 