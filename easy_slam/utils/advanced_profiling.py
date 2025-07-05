import time
import psutil
import threading
import numpy as np
from collections import defaultdict, deque
import matplotlib.pyplot as plt

class PerformanceProfiler:
    """
    Advanced performance profiler for SLAM systems.
    Tracks timing, memory, CPU usage, and bottlenecks.
    """
    def __init__(self, max_history=1000):
        self.max_history = max_history
        self.timings = defaultdict(lambda: deque(maxlen=max_history))
        self.memory_usage = deque(maxlen=max_history)
        self.cpu_usage = deque(maxlen=max_history)
        self.fps_history = deque(maxlen=max_history)
        self.timestamps = deque(maxlen=max_history)
        
        self.start_time = time.time()
        self.last_frame_time = self.start_time
        self.frame_count = 0
        
        # Thread-safe locks
        self.timing_lock = threading.Lock()
        self.memory_lock = threading.Lock()
        
        # Start monitoring thread
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_system, daemon=True)
        self.monitor_thread.start()

    def start_timer(self, module_name):
        """Start timing a module."""
        return time.time()

    def end_timer(self, module_name, start_time):
        """End timing a module and record the duration."""
        duration = time.time() - start_time
        with self.timing_lock:
            self.timings[module_name].append(duration)
        return duration

    def record_frame(self):
        """Record a new frame and update FPS."""
        current_time = time.time()
        self.frame_count += 1
        
        if self.frame_count > 1:
            fps = 1.0 / (current_time - self.last_frame_time)
            self.fps_history.append(fps)
        
        self.last_frame_time = current_time
        self.timestamps.append(current_time - self.start_time)

    def _monitor_system(self):
        """Monitor system resources in background thread."""
        process = psutil.Process()
        
        while self.monitoring:
            try:
                # Memory usage
                memory_info = process.memory_info()
                memory_mb = memory_info.rss / 1024 / 1024
                
                with self.memory_lock:
                    self.memory_usage.append(memory_mb)
                
                # CPU usage
                cpu_percent = process.cpu_percent()
                self.cpu_usage.append(cpu_percent)
                
                time.sleep(0.1)  # Sample every 100ms
                
            except Exception as e:
                print(f"[Profiler] Error monitoring system: {e}")
                break

    def get_module_stats(self, module_name):
        """Get statistics for a specific module."""
        with self.timing_lock:
            if module_name not in self.timings:
                return None
            
            times = list(self.timings[module_name])
            if not times:
                return None
            
            return {
                'mean': np.mean(times),
                'std': np.std(times),
                'min': np.min(times),
                'max': np.max(times),
                'median': np.median(times),
                'count': len(times)
            }

    def get_system_stats(self):
        """Get current system statistics."""
        with self.memory_lock:
            current_memory = self.memory_usage[-1] if self.memory_usage else 0
            avg_memory = np.mean(list(self.memory_usage)) if self.memory_usage else 0
        
        current_cpu = self.cpu_usage[-1] if self.cpu_usage else 0
        avg_cpu = np.mean(list(self.cpu_usage)) if self.cpu_usage else 0
        
        current_fps = self.fps_history[-1] if self.fps_history else 0
        avg_fps = np.mean(list(self.fps_history)) if self.fps_history else 0
        
        return {
            'memory_mb': current_memory,
            'avg_memory_mb': avg_memory,
            'cpu_percent': current_cpu,
            'avg_cpu_percent': avg_cpu,
            'fps': current_fps,
            'avg_fps': avg_fps,
            'frame_count': self.frame_count,
            'uptime_seconds': time.time() - self.start_time
        }

    def get_bottlenecks(self, threshold_percentile=95):
        """Identify performance bottlenecks."""
        bottlenecks = []
        
        with self.timing_lock:
            for module_name, times in self.timings.items():
                if not times:
                    continue
                
                times_list = list(times)
                percentile_time = np.percentile(times_list, threshold_percentile)
                mean_time = np.mean(times_list)
                
                if percentile_time > mean_time * 2:  # Significant spikes
                    bottlenecks.append({
                        'module': module_name,
                        'percentile_time': percentile_time,
                        'mean_time': mean_time,
                        'spike_factor': percentile_time / mean_time
                    })
        
        return sorted(bottlenecks, key=lambda x: x['spike_factor'], reverse=True)

    def generate_report(self, save_path=None):
        """Generate a comprehensive performance report."""
        report = []
        report.append("=" * 50)
        report.append("EASY-SLAM PERFORMANCE REPORT")
        report.append("=" * 50)
        
        # System stats
        sys_stats = self.get_system_stats()
        report.append(f"\nSYSTEM STATISTICS:")
        report.append(f"  Uptime: {sys_stats['uptime_seconds']:.1f} seconds")
        report.append(f"  Total Frames: {sys_stats['frame_count']}")
        report.append(f"  Current FPS: {sys_stats['fps']:.1f}")
        report.append(f"  Average FPS: {sys_stats['avg_fps']:.1f}")
        report.append(f"  Current Memory: {sys_stats['memory_mb']:.1f} MB")
        report.append(f"  Average Memory: {sys_stats['avg_memory_mb']:.1f} MB")
        report.append(f"  Current CPU: {sys_stats['cpu_percent']:.1f}%")
        report.append(f"  Average CPU: {sys_stats['avg_cpu_percent']:.1f}%")
        
        # Module stats
        report.append(f"\nMODULE TIMING STATISTICS:")
        with self.timing_lock:
            for module_name in sorted(self.timings.keys()):
                stats = self.get_module_stats(module_name)
                if stats:
                    report.append(f"  {module_name}:")
                    report.append(f"    Mean: {stats['mean']*1000:.2f} ms")
                    report.append(f"    Std: {stats['std']*1000:.2f} ms")
                    report.append(f"    Min: {stats['min']*1000:.2f} ms")
                    report.append(f"    Max: {stats['max']*1000:.2f} ms")
                    report.append(f"    Count: {stats['count']}")
        
        # Bottlenecks
        bottlenecks = self.get_bottlenecks()
        if bottlenecks:
            report.append(f"\nPERFORMANCE BOTTLENECKS:")
            for bottleneck in bottlenecks[:5]:  # Top 5
                report.append(f"  {bottleneck['module']}: {bottleneck['spike_factor']:.1f}x spike")
        
        report_text = "\n".join(report)
        
        if save_path:
            with open(save_path, 'w') as f:
                f.write(report_text)
        
        return report_text

    def plot_performance(self, save_path=None):
        """Generate performance plots."""
        if not self.timestamps:
            return "No data to plot"
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # FPS over time
        if self.fps_history:
            axes[0, 0].plot(list(self.timestamps)[-len(self.fps_history):], list(self.fps_history))
            axes[0, 0].set_title('FPS Over Time')
            axes[0, 0].set_ylabel('FPS')
            axes[0, 0].grid(True)
        
        # Memory usage over time
        if self.memory_usage:
            axes[0, 1].plot(list(self.timestamps)[-len(self.memory_usage):], list(self.memory_usage))
            axes[0, 1].set_title('Memory Usage Over Time')
            axes[0, 1].set_ylabel('Memory (MB)')
            axes[0, 1].grid(True)
        
        # CPU usage over time
        if self.cpu_usage:
            axes[1, 0].plot(list(self.timestamps)[-len(self.cpu_usage):], list(self.cpu_usage))
            axes[1, 0].set_title('CPU Usage Over Time')
            axes[1, 0].set_ylabel('CPU (%)')
            axes[1, 0].grid(True)
        
        # Module timing box plot
        with self.timing_lock:
            if self.timings:
                module_data = []
                module_names = []
                for module_name, times in self.timings.items():
                    if times:
                        module_data.append(list(times))
                        module_names.append(module_name)
                
                if module_data:
                    axes[1, 1].boxplot(module_data, labels=module_names)
                    axes[1, 1].set_title('Module Timing Distribution')
                    axes[1, 1].set_ylabel('Time (seconds)')
                    axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig

    def stop(self):
        """Stop profiling and monitoring."""
        self.monitoring = False
        if self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=1.0)

class ProfilerContext:
    """Context manager for easy profiling."""
    def __init__(self, profiler, module_name):
        self.profiler = profiler
        self.module_name = module_name
        self.start_time = None
    
    def __enter__(self):
        self.start_time = self.profiler.start_timer(self.module_name)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.profiler.end_timer(self.module_name, self.start_time)

def profile_module(profiler, module_name):
    """Decorator for profiling module functions."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            with ProfilerContext(profiler, module_name):
                return func(*args, **kwargs)
        return wrapper
    return decorator 