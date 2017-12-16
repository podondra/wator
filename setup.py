from setuptools import setup
from Cython.Build import cythonize
import numpy


setup(
        name='wator',
        version='0.3',
        description='Wa-Tor population dynamics simulation',
        author='Ondřej Podsztavek, Miro Hrončok',
        author_email='ondrej.podsztavek@gmail.com',
        license='GNU General Public License v3.0',
        ext_modules=cythonize('wator/cwator.pyx', language_level=3),
        include_dirs=[numpy.get_include()],
        setup_requires=['Cython', 'NumPy', 'PyQt5'],
        install_requires=['NumPy'],
        )
