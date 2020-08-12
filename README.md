# shelper-flask

Description
-----------
This site is designed to store a data for people involved in sport. It is designed to be as easy to use as possible. You can save new exercises by simply naming it and assigning it to a specific muscle category. If the exercise is outdated for you, it will be even easier to delete it. Just one click on the title. To add training, simply select the previously saved exercises and add them to the fixing list. Practically everything on this site you can do just in one click.

Manual
------
It should be said that the front-end is not the strong point of this site. But on the other hand, this site has protection against CSRF attacks and reliable authentication, implemented through the JWT, and proxying requests to the site is processed using nginx. All services for this site are laid out in a docker containers. This means that you can deploy it anywhere very quickly, just following the instructions below.


After cloning this repository locally, be sure to add yourself .env file with important keys inside current folder. In the following formats:


* SECRET_CSRF_KEY = 'secret'
* JWT_SECRET_KEY = 'secret'
* POSTGRES_USER = 'user'
* POSTGRES_PASSWORD = 'pass'
* POSTGRES_DB = 'database'
* MAIL_USERNAME = 'sporthelper@gmail.com'
* MAIL_PASSWORD = 'mailpassword'
  
Afterwards up docker-compose and check http://0.0.0.0/


