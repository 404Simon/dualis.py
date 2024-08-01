# Unofficial Dualis Python API Wrapper

A Third-Party Python API Wrapper for [https://dualis.dhbw.de/](https://dualis.dhbw.de/)
This is a fork of the original but deleted project by [pvhil](https://github.com/pvhil).

## Usage

```python
import dualis

# initialize and login

test = dualis.Dualis("email", "pass")

# or login later:

test = dualis.Dualis()
test.login("email","pass")
```
 Methods should be self-explanatory.


## Intentions

This module was created with good intentions behind it, for example:

- Learning to code with Python
- Learning to work with APIs and modules
- Implementing timetables or other information in own applications

Please do not abuse this project to harm the original website in any way.  
I am not responsible for any harm caused with this project. Please use this API wrapper with caution and do not spam request the Dualis Server.

## Todo

Only the `get_time_table_week` method is really usable at the moment.
Thats what i wrote and thats the only one with tests too.

## Contributing

Do it!

## Disclaimer

The Website [https://dualis.dhbw.de/](https://dualis.dhbw.de/) is a product from the [corporate state university baden württemberg (Duale Hochschule Baden-Würrtemberg)](https://www.dhbw.de/english/home).

The Project "dualis.py" is a third-party application and not affiliated with the [corporate state university baden württemberg](https://www.dhbw.de/english/home) in any way.

Licensed with the MIT-License 2023 pvhil
