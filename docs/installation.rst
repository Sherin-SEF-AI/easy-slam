Installation Guide
==================

EasySLAM can be installed in several ways. Choose the method that best suits your needs.

From PyPI (Recommended)
-----------------------

The easiest way to install EasySLAM is using pip:

.. code-block:: bash

   pip install easy-slam

This will install the latest stable version with all required dependencies.

From Source
-----------

If you want to install from the latest development version or contribute to the project:

.. code-block:: bash

   git clone https://github.com/Sherin-SEF-AI/easy-slam.git
   cd easy-slam
   pip install -e .

Development Installation
------------------------

For development work, you can install in editable mode with development dependencies:

.. code-block:: bash

   git clone https://github.com/Sherin-SEF-AI/easy-slam.git
   cd easy-slam
   pip install -e ".[dev]"

Or use the provided development script:

.. code-block:: bash

   chmod +x scripts/install_dev.sh
   ./scripts/install_dev.sh

Dependencies
------------

EasySLAM automatically installs the following core dependencies:

* **OpenCV** (>=4.5.0) - Computer vision library
* **NumPy** (>=1.20.0) - Numerical computing
* **PyQt6** (>=6.0.0) - GUI framework
* **Matplotlib** (>=3.3.0) - Plotting and visualization
* **SciPy** (>=1.7.0) - Scientific computing

Optional dependencies (installed as needed):

* **PyRealSense2** - Intel RealSense camera support
* **ultralytics** - YOLOv8 for semantic mapping
* **open3d** - 3D point cloud processing
* **quaternion** - Quaternion mathematics

System Requirements
------------------

* **Python**: 3.8 or higher
* **Operating System**: Linux, macOS, or Windows
* **Memory**: At least 4GB RAM (8GB recommended)
* **Storage**: 2GB free space for installation

Hardware Requirements
--------------------

* **Camera**: USB webcam or Intel RealSense camera
* **GPU**: Optional, but recommended for real-time processing
* **CPU**: Multi-core processor recommended

Troubleshooting
---------------

Common installation issues and solutions:

**PyQt6 Installation Issues**
   If you encounter issues installing PyQt6, try:

   .. code-block:: bash

      pip install PyQt6-Qt6 PyQt6-sip

**OpenCV Installation Issues**
   For OpenCV installation problems:

   .. code-block:: bash

      pip install opencv-python opencv-contrib-python

**RealSense Camera Issues**
   If you have problems with RealSense cameras:

   .. code-block:: bash

      pip install pyrealsense2

**Permission Issues**
   If you get permission errors, use:

   .. code-block:: bash

      pip install --user easy-slam

Verification
------------

After installation, verify that EasySLAM works correctly:

.. code-block:: python

   from easy_slam import EasySLAM
   print("EasySLAM imported successfully!")

Or run the test script:

.. code-block:: bash

   python test_package.py 