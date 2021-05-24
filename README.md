### Walking from Home

With the emergence of Hybrid and more flexible working post covid, the importance of social interaction and physical excersize becomes even more important for home workers. Walking From Home will offer a platform for home workers to share walking routes, form walking groups and arrange to meet for one off or regular walks.

The API provides the backend for the website and is hosted in Heroku.

A very basic front end has been developed using Vuetify, Vue and Veuex. This is hosted in ..............


## Getting Started

### Backend API Hosting

#### Heroku Endpoint

The backend can be accessed at https://walkingfromhome.herokuapp.com/

#### Endpoints

There a are four main endpoints for the API

/walkers    contains details of the registered walkers
/groups     contains details of groups of walkers
/routes     contains details of the walking routes
/events     contains details of walking events

The endpoints are explained in more detail below.

#### Authentication

Authentication is handled by Auth0. The site will not show any details unless the user has regstered. Further functionality is restricted by the application of user roles. There are two roles WFH-User and WFH-Admin. The admin role allows full permissions to create, edit, delete on all endpoints.

Two test accounts have been setup:-

wfhuser@gmail.com - which is assigned the WFH-User role
wfhadmin@gmail.com - which is assigned the WFH-Admin role

both users have password WalkingFromH0me!

#### Front End Hosting

A basic front end has been developed to show the login page and redirection working and very basic restriction of data access. You can only view each section if you are logged in.

The front end can be found at https://walking-from-home.web.app/

Press the login button top left and use the credentials above.

From the menu select Profile to view the persmissions for each user extracted from the Auth0 JWT.

