# project setup

# after clone project use below command
 -  cd user_management/

# create venv and actviate for windows
 - python -m venv venv
 - .venv\Scripts\activate

# install packages
 - pip install -r requirement.txt

# after installation all packages you have create table for that you have to run below command
 - python manage.py makemigrations
   (for example - (venv)C:\Users\dheeraj\Desktop\users_management>python manage.py makemigrations)

 - python manage.py migrate

# command for create superuser
 - python manage.py createsuperuser

# for start server
 - python manage.py runserver
 
# after creating super user you have to login 
 - http://127.0.0.1:8000/admin/ - here you will see all created tables

# To See Api Documentation You have serve below url
note: before serving this url you have to login with superuser credentials
 - http://127.0.0.1:8000/api/doc

