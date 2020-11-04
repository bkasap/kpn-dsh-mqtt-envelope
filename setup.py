import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='kpn-dsh-mqtt-envelope',
    version='0.2.3',
    author='Bahadir Kasap',
    author_email="bkasap@gmail.com",
    description="Envelope wrapper/unwrap for kpn-dsh-mqtt-envelopes",
    url="https://github.com/bkasap/kpn-dsh-mqtt-envelope",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=("test", "test.*")),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
    install_requires=['googleapis-common-protos'],
    zip_safe=False
)