# Dualis Python API Wrapper

A Python API Wrapper for [https://dualis.dhbw.de/](https://dualis.dhbw.de/)

## Usage

```python
import dualis

# initialize and login

test = dualis.Dualis("email", "pass")

# or login later:

test = dualis.Dualis()
test.login("email","pass")

# get parsed information

print(test.getExamResults())
print(test.getNewMessages())
print(test.getPerformance())
print(test.getTimeTable())
print(test.getTodayEvents())
print(test.getExamResults())
...
```

## Why do I need it?

If you want to create an application like a mobile app, chatbot, website or something else in python, you can use this module to easily receive parsed information (like your timetable) to implement it in your application.

## Disclaimer

This module was created with good intentions behind it, for example:

- Learning to code with Python
- Learning to work with APIs and modules
- Implementing timetables or other information in own applications

Please do not abuse this project to harm to original website in any way.  
I am not responsible for any harm caused with this project. Please use this API wrapper with caution and do not spam request the Dualis Server.

## Todo

- Implement more Endpoints
- Better, more precise Parsing
- Make Return values more readable
- Documentation

Please Contribute if you can

## Contributing

I can not parse information from the website completely, because i do not have full access to timetables and other information.  
If you have a completed timetable with many appointments, please contribute to this project to make the parsing more precise.
  
Licensed with the MIT-License 2023 pvhil
