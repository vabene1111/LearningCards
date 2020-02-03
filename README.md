A simple django based application to create, share and play online quizzes.
Everything is based on self control (like learning cards) and is not meant as a actual quiz/test platform.

**Features**
- Create Questions in different courses, chapters and organizations
- Quiz where questions are presented based on previously answered questions
- Tests where each questions of a course is asked once
- Optimized for mobile usage
- Statistics that show you how good you did on different courses
- Anonymous playing or creation of accounts that track question progress
- Markdown for questions, answers and comments

## Disclaimer
This application has been developed mainly for my personal use during exam preparation (where time is short) and 
thus the focus was on features and not on code style or maintainability. 

Everything, including this readme, is rather "quick and dirty" but it works.

## Install

### Docker-Compose
When cloning this repository, a simple docker-compose file is included. It is made for setups already running an nginx-reverse proxy network with let’s encrypt companion but can be changed easily. Copy `.env.template` to `.env` and fill in the missing values accordingly.  
Now simply start the containers and run the `update.sh` script that will apply all migrations and collect static files.
Create a default user by executing into the container with `docker-compose exec web_quiz sh` and run `python3 manage.py createsuperuser`.

### Manual
Copy `.env.template` to `.env` and fill in the missing values accordingly.  
You can leave out the docker specific variables (VIRTUAL_HOST, LETSENCRYPT_HOST, LETSENCRYPT_EMAIL). 
Make sure all variables are available to whatever serves your application.

Otherwise simply follow the instructions for any django based deployment
(for example this one http://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html).