.. easy-slam documentation master file

Welcome to EasySLAM's documentation!
=====================================

🚀 **EasySLAM** is a production-ready Python package that makes Simultaneous Localization and Mapping (SLAM) accessible to everyone. Whether you're a beginner exploring robotics or an advanced user building complex autonomous systems, EasySLAM provides the tools you need.

.. image:: https://img.shields.io/pypi/v/easy-slam.svg
   :target: https://pypi.org/project/easy-slam/
   :alt: PyPI version

.. image:: https://img.shields.io/github/license/Sherin-SEF-AI/easy-slam.svg
   :target: https://github.com/Sherin-SEF-AI/easy-slam/blob/main/LICENSE
   :alt: License

.. image:: https://img.shields.io/github/stars/Sherin-SEF-AI/easy-slam.svg
   :target: https://github.com/Sherin-SEF-AI/easy-slam
   :alt: GitHub stars

Quick Start
-----------

Install EasySLAM:

.. code-block:: bash

   pip install easy-slam

Basic usage:

.. code-block:: python

   from easy_slam import EasySLAM

   # Initialize with webcam and ORB-SLAM
   slam = EasySLAM(sensor='webcam', algorithm='orb_slam')

   # Start processing
   slam.start()

   # Stop when done
   slam.stop()

Launch the GUI:

.. code-block:: bash

   easy-slam-gui

Key Features
------------

* **Multiple Sensor Support**: Webcam, RealSense, stereo cameras, LiDAR, and dataset playback
* **Advanced Algorithms**: ORB-SLAM, FastSLAM, GraphSLAM, Visual-Inertial SLAM, RGB-D SLAM
* **Beautiful GUI**: Modern PyQt6-based interface with real-time visualization
* **Easy CLI**: Command-line interface for quick experiments and automation
* **Semantic Mapping**: YOLOv8 integration for object detection
* **Performance Profiling**: Real-time monitoring and detailed analytics

Installation
------------

From PyPI (Recommended):

.. code-block:: bash

   pip install easy-slam

From Source:

.. code-block:: bash

   git clone https://github.com/Sherin-SEF-AI/easy-slam.git
   cd easy-slam
   pip install -e .

Documentation Contents
----------------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   user_guide
   api_reference
   examples
   contributing

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

External Links
--------------

* `GitHub Repository <https://github.com/Sherin-SEF-AI/easy-slam>`_
* `PyPI Package <https://pypi.org/project/easy-slam/>`_
* `Issue Tracker <https://github.com/Sherin-SEF-AI/easy-slam/issues>`_
* `Discussions <https://github.com/Sherin-SEF-AI/easy-slam/discussions>`_

API Reference
-------------

.. automodule:: easy_slam
    :members:
    :undoc-members:
    :show-inheritance: 