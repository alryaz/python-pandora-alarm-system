import setuptools


setuptools.setup(
    name="pandora-alarm-system",
    version="0.0.1",
    description="Pandora CAS Python API",
    long_description=open("README.md").read().strip(),
    author="Alexander Ryazanov",
    author_email="alryaz@xavux.com",
    py_modules=["pandora_alarm_system"],
    install_requires=[],
    license="MIT License",
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
