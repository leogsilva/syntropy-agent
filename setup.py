from setuptools import setup, find_packages

setup(
    name="platform-agent",
    version='0.0.2',
    py_modules=['platform-agent'],
    install_requires=[
        'pyroute2==0.5.12',
        'websocket-client==0.57.0',
        'requests==2.22.0',
        'PyNaCl==1.0.1',
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'noia_agent = platform_agent.__main__:main'
        ]
    },
)
