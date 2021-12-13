# Project of the website for mr. Jozef Wielogorka. Personal website of honey seller.

## Collaboration with [Sebastian Banz](https://github.com/derbanz) 


### TECHNOLOGIES USED:
- HTML
- CSS
- SASS
- JavaScript
- Django
- Python

### GOALS
* ✔️ responsive webdesign
* ✔️ performance, accessibility, SEO, best practices above 90%
* ✔️ individual and original design
* ✔️ keeping design simple and clean
* ✔️ allowing dynamic content addition

### LINKS

* FIGMA [WIREFRAME](https://www.figma.com/file/TAsoIHnEvvr3AzdgYl512R/Honey?node-id=0%3A1)
* [LIVE WEBSITE](https://www.wielomiod.pl)

### Setup
To properly run this project, follow these steps.
* Install python 3.x and pip
* Install the packages listed in requirements.txt -> `pip install -r requirements.txt`
* Adjust the python path in jozef_wielogorka/manage.py to point to the correct location
* Optionally create local settings with a secure key, Debug option, Email and logging details
* Update your database with the current model by migrating (do this whenever there's a bigger change to the models.py file) using `./manage.py makemigrations` and `./manage.py migrate`
* Run the website locally using the runserver command, you can then access the website under localhost:8000 -> `./manage.py runserver`
* Access the admin panel under \<url\>/admin. Setup an admin account using `./manage.py createsuperuser`
