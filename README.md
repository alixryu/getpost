# firelands
A bare minimum starting package for a python flask based web server development.
Available for forking and expanding.

## Flask Project Done Right
A flask project, small or large, should be built with the following:
* pip
* virtualenv
* nose
* pep8/flake8
* blueprint
* sphinx

Based on additional needs, a flask project should have:
* sqlalchemy (if using a DBMS)

### pip/virtualenv
* only sudo install virtualenv
* requrements.txt

install libraries for project
``` shell
pip install -r requirements.txt
```
update requirements.txt
``` shell
pip freeze > requirements.txt
```

## nose
* unit testing for everyone
* [nose documentation](https://nose.readthedocs.org/en/latest/)

### flake8
* combination of PyFlakes, pep8, and McCabe

### blueprint
* fast modularizing

### sphinx
* documentation for your application

### sqlalchemy
* THE Object Relational Mapper of choice

## Project Guideline
\*   master : minimum : static web page (flask, nose, flake8, blueprint, sphinx)  
|\  
| * alchemist : database : basic dynamic server (sqlalchemy)  

---
## About the project title
Firelands is an apartment building at Oberlin College, OH. Known to be a senior
dorm, it hosts seniors who want to live in singles and want to be left alone to
focus on their work while having a peaceful year until their graduation. Despite
being a decent college housing option and its popularity among Oberlin students,
Firelands is a bare minimum living space that asks for some decoration and
attention. With Firelands, you can create the perfect personal office, a great
cocktail party room, or both.
