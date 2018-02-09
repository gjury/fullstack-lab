# fullstack-lab
This repo is for BriteCore to review as part of an exercise project

## Problem
This solution provides the visualization of data that describes different assets required to provide insurance for. The data presented are values for different instances and the type of data that the insurer elected to describe that asset. The form is not submitable to be persisted.

### Data
> Deliverables will be either...
- [x] A [Python file](https://github.com/gjury/fullstack-lab/blob/master/app.py) containing the ORM classes for these tables.
- [x] An entity relationship diagram, which depicts the tables and their relationship to one another.
![](https://i.imgur.com/LID9QLp.png)
- [x] Both 1 and 2, because you're awesome.

### Backend
> Deliverables will be...
- [x] A well-tested REST API written in Python.

There are 2 [APIS](https://github.com/gjury/fullstack-lab/blob/master/app.py), 
  * first one will retrieve all the Risks available
  
  `/risks/`
  
  * The second one will get all the data for the chosen Risk
  
  `/risk/{idOfRisk}/`


### Frontend
> Deliverables will be...
- [x] Mega bonus points** if you use Vue.js specifically.
- [x] Mega bonus points** if you the app in [AWS Lambda]

In order to keep it simple I used CDN for all the js libraries.

### Live
Please note that the first request to be made, needs to be this one, so some data is created to render in the frontend.
https://ne8g9tixsj.execute-api.us-east-1.amazonaws.com/dev/initdb

Once that link provides an ok message, the app can be visited:

### https://ne8g9tixsj.execute-api.us-east-1.amazonaws.com/dev/

Also, please note that the domain in the url might change once the lambda is destroyed, or the app is undeployed with zappa, so please if the url doesnt work for you, please let me know.

Thanks!, best Regards.











