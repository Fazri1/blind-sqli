This script is from PortSwigger, and I upgrade it.
This script will brute force every single character of password in users table, with alphanumeric and special character.  

To use this script you need to know some information:
- Is website vulnerable to SQLi attack
- Vulnerable parameter
- True or false condition in web response (in text or web content)
- Cookie
- Session Id
- Exist database table
- Exist column in database table
- Exist username in user table (if user table exist)
- Password length (if password column exist in user table

If even one of the conditions above is not met, the script will not work.
