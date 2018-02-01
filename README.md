# Username Finder

This python script will help those interested in finding short, unique usernames on platforms. It was initially built to find the shortest available username on GitHub, but it has been generalized to work on any platform that returns a HTTP 404 error message when a user does not exist.

## Usage
In order to use the username finder, download the script in this repo and run it with the following commands:

```
python find_username {THREAD COUNT} {LETTER COUNT} {BASE URL}
```
*THREAD COUNT* = the number of individual threads you want requesting the base url

*LETTER COUNT* = the length of the user name you are looking platform

*BASE URL* = the base URL to access user accounts. i.e. https://github.com/ (note the trailing forward slash)
