  Hi! My name is Eugene. You are welcome here! Contact me via [email](mailto:eugene.osakovich@gmail.com)
 
 # Support API project
 
 ## SUMMARY:
 #### This API is for maintain workflow of Tech Support Service

 #### Here you can create Issue, track its status and communicate with support team through leaving comments.
 
 #### Technologies: Python, Django, DjangoRestFramework, Postgres, JWT auth, PyTest, Celery+Redis+Flower and Docker
 
 ## API Schema:
 
#### Issue endpoint:
![issue](https://user-images.githubusercontent.com/67389118/173232316-d7cd043c-ca25-42b8-ac5c-e36680205c60.jpg)
#### User endpoint:
![user](https://user-images.githubusercontent.com/67389118/173232324-1fd31f0d-d3c1-421d-934b-b3349322c08d.jpg)

## Run and go:
- git clone the project
 
      gh repo clone sheirand/support_api_v2

- add smtp host (if u want email notification feature up)

  ```EMAIL_USE_TLS=True
     EMAIL_HOST="smtp.some-mail.com"
     EMAIL_HOST_USER="your-user@some-mail.com"
     EMAIL_HOST_PASSWORD="your-password"
     EMAIL_PORT=port
     ```
     
- enter the docker-compose up on project directory
    
      docker-compose up

- project is now available on your  [http://127.0.0.1:8000/]

- you can look API schema on [http://127.0.0.1:8000/schema/]

- if you want to ensure that everything is working fine:

      docker-compose exec web pytest
 
- if you want to create a superuser:
 
      docker-compose exec web python manage.py createsuperuser


## More closer look:

#### Detailed list of project features:

- Support API consists of 3 services:
  - user endpoint
  - issue endpoint (include comments)
  - celery+redis for async email notification
- PostgreSQL is used as database for:
  - user model
  - issue model
  - comment model
- Redis is used as message broker for Celery 
- Celery is used for async email notification
- Custom User model: 
  - no usernames, only email
  - permissions based on user classes: superuser (admin), staff (support team), users
  - authentication based on JWT in cookies

- Permissions:
  - user can:
    - register/login/logout/see his profile
    - create issues
    - see his own issues
    - leave comments on issues
    - see all comments on his issues
    - recieve email notification if status of his issue has been change
  - staff inherits user and can:
    - see all issues posted
    - change issue status
    - assign issues only on staff
    - edit issues
    - leave comment on all issues
    - see all comments on all issues
  - admin inherits staff and can:
    - create users and staff
    - delete and edit users information
    - delete and edit issues and comments

[email]: eugene.osakovich@gmail.com
