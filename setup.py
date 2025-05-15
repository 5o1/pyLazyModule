from setuptools import setup, find_packages

with open("LICENSE", "r") as file:
    license_content = file.read()

setup(
    name="pylazymodule",
    version="0.0.1",
    description="A simple practice of dynamic module loader to avoid explicitly importing optional dependencies when a module is not accessed. This is useful when using multiple optional backends for deep learning.",
    author="5o1",
    author_email="assanekowww@gmail.com",
    url="https://github.com/5o1/pyLazyModule",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True, 
    python_requires=">=3.9",
    license=license_content,
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)