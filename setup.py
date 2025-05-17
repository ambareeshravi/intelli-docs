from setuptools import setup, find_packages

def read_requirements(filename):
    """
    Read requirements from a file
    """
    with open(filename) as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Read requirements from requirements.txt
install_requires = read_requirements('requirements.txt')

# Read development requirements
dev_requires = read_requirements('requirements-dev.txt')

setup(
    name="intelli_docs",
    version="0.1.0",
    packages=find_packages(),
    install_requires=install_requires,
    extras_require={
        "dev": dev_requires,
    },
    author="Ambareesh Ravi",
    description="An intelligent document Q&A system using LLMs, RAG, and MCP",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ambareeshravi/intelli-docs.git",  # Update this
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.9",
) 