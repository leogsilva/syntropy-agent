from setuptools import setup, find_packages, Extension


from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name="platform-agent",
    version='0.0.53',
    py_modules=['platform-agent'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'pyroute2==0.5.12',
        'websocket-client==0.57.0',
        'requests==2.22.0',
        'PyNaCl==1.3.0',
        'docker-py==1.10.6',
        'icmplibv2==1.0.5',
        'PyYAML==5.3.1',
        'dnspython==1.16.0',
        'iperf3==0.1.11',
        'prometheus-client==0.8.0'
    ],
    packages=find_packages(),
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    entry_points={
        'console_scripts': [
            'noia_agent = platform_agent.__main__:main'
        ]
    },
)
