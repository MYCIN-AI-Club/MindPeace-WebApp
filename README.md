# MindPeace Habit Tracker App

## Project Documentation 


## Description 
MindPeace Web Application is designed to help you track all your habits. Each logged in user can create and manage multiple types of trackers(like running, sleeping ,etc) and keep a note of your daily life.. The user can access all different habits from the dashboard  and can add more logs to it , add more trackers, and view their progress . 

### Technologies used 
1. flask {for application framework} 
    • Flask 
    • url_for 
    • render_template 
    • redirect 
    • request 
2. Flask_SQLAlchemy 
3. Bootstrap  
4. HTML
5. CSS
6. Matplotlib{for plotting graphs}
7. Datetime{for timestamp}

### DB Schema Design 
1. User Table 

|Column  | Data type | Constraints       | Description|
|--------|-----------|-------------------|------------|
|id      |   Integer | Primary key       | User Id    |
|username| String(30)| Unique , not null | User Name  |
|password|String (30)| Not null          | Password   |

2. Trackers
Column      | Data type | Constraints              | Description
id          | Integer   | Primary Key              |     Id
name        | String(30)| Not null                 | Tracker Name
description |String(100)|       -                  | Description of tracker type
last_update | DateTime  | Not null                 | When was tracker last updated
user_id     | Integer   | Foreign Key from User    |  User Id
                            Table, Not null



3. Logs
Column      | Data type | Constraints                   | Description
id          | Integer   | Primary Key                   |     Id
when        | DateTime  |       -                       | When was this log added
value       | Float     |   Not null                    | Value that we want to add in log
notes       | String    |       -                       | Any remarks about the log
tracker_id  | Integer   | Foreign Key from tracker Table| Tracker id



### Architecture and Features 

The main control of the application is in file ‘main.py’. 
The template folder contains all the html files. 
The static folder contains css style sheets and the ‘images‘  folder which contains images  used in the project. 
‘trackdb.sqlite3’ contains the database. 

