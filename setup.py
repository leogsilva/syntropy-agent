from setuptools import setup, find_packages

setup(
    name="platform-agent",
    version='0.0.25',
    py_modules=['platform-agent'],
    install_requires=[
        'pyroute2==0.5.12',
        'websocket-client==0.57.0',
        'requests==2.22.0',
        'PyNaCl==1.3.0',
        'docker-py==1.10.6',
        'icmplibv2==1.0.5'
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'noia_agent = platform_agent.__main__:main'
        ]
    },
)
