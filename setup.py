import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires=[
    'require-python-3',
    'bardapi',
    'EdgeGPT',
    'openai'
        ]

setuptools.setup(
    name="CAI",
    version="1.0.0",
    author="Alireza Farshin",
    author_email="alireza.farshin@gmail.com",
    install_requires=install_requires,
    description="CodeAI (CAI)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aliireza/cai",
    packages=setuptools.find_packages(where='src', exclude=['tests']),
    package_dir={'': 'src'},
    package_data={},
    py_modules=['cai'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL-3.0 license",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    entry_points = {
              'console_scripts': [
                  'cai=src.cai:main',
              ],
          },
)