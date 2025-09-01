from setuptools import setup, find_packages

setup(
    name="EUnix",  # Replace with your project name
    version="0.1.0",
    author="Godwin Okwuibe",
    author_email="godwin.okwuibe@gmail.com",
    description="A Market platform that will be able to match buyers and sellers of electricity",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/my_project",  # Replace with your GitHub repo URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=open("requirements.txt").read().splitlines(),
)