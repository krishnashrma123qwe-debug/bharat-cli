from setuptools import setup, find_packages

setup(
    name="bharat-cli",
    version="1.0.0",
    description="Terminal AI Pair Programmer & Code Review Agent powered by BharatCode Qwen 3.8 27B",
    author="Krishna Sharma",
    author_email="krishnashrma123qwe@gmail.com",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
        "rich>=13.0.0",
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "bharat=bharat.cli:cli",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Software Development :: Code Generators",
    ],
    python_requires=">=3.8",
)
