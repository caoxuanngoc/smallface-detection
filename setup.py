import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    python_requires='>=3.5.5',
    install_requires=["numpy>=1.14.0", "gdown>=3.10.1", "Pillow>=5.2.0", "opencv-python>=3.4.4", "tensorflow>=1.9.0", "math", "cv2", "pathlib", "warnings", "tkinter", "matplotlib", "mtcnn" ]
)