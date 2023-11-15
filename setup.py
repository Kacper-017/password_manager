from setuptools import setup

setup(
    name='password_manager',
    version='0.1',
    packages=['password_manager'],
    entry_points={
        'console_scripts': [
            'password_manager=password_manager.__main__:main'
        ]
    },
    install_requires=[
        'cryptography',
        'pyperclip'
    ],
    author='Kacper Masny',
    author_email='your.email@example.com',
    description='A password manager',
    license='MIT',
    keywords='password manager',
    url='https://github.com/Kacper-017/password_manager'
)

