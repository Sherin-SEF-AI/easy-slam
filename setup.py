from setuptools import setup, find_packages

setup(
    name='easy-slam',
    version='0.1.0',
    description='Beginner-friendly yet powerful SLAM library for robotics and research',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='sherin joseph roy',
    author_email='sherin.joseph2217@gmail.com',
    url='https://github.com/Sherin-SEF-AI/EasySLAM',
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=[
        'numpy',
        'opencv-python',
        'scipy',
        'matplotlib',
        'pyyaml',
    ],
    extras_require={
        '3d': ['open3d'],
        'realsense': ['pyrealsense2'],
        'g2o': ['python-g2o'],
        'dev': ['pytest', 'sphinx', 'jupyter', 'black', 'flake8'],
        'gui': ['PyQt6'],
    },
    entry_points={
        'console_scripts': [
            'easy-slam=easy_slam.__main__:main',
            'easy-slam-gui=easy_slam.gui.__main__:main',
        ],
    },
    include_package_data=True,
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    project_urls={
        'Source': 'https://github.com/Sherin-SEF-AI/EasySLAM',
    },
) 