import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aim_target_clustering",
    version="0.0.1",
    author="Equinor",
    author_email=".@equinor.com",
    description="Target clustering algorithm for the AI for Maturation project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/equinor/aim-target-clustering",
    project_urls={
        "Bug Tracker": "https://github.com/equinor/aim-target-clustering/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    install_requires=["requests"],
    python_requires=">=3.6",
)