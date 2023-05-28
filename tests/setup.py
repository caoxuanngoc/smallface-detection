from distutils.core import setup
import py2exe
setup(windows=["app.py"], packages=['dataset','output_mtcnn','output_retinaface'])