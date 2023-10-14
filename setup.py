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
    classifiers=["Packages"],
)
