### Basic Repository Design Pattern Illustration with SQLAlchemy ###

The goal of this project is to get you acquainted with an implementation of the Repository Design pattern.<br>
We will do that through an Object Relationnal Mapping (ORM) Framework called SQLAlchemy.<br>
Alchemy natively implements a Data Mapper Design Pattern, on top of which this project adds a Repository Layer, to be able to switch from one Database Endpoint to Another. To illustrate this we will use 2 databases : SQLLite, and MySQL/MariaDB.<br>

#### How to Approach the Project ####

Start by taking a look to the UML Class diagram in the uml folder.
Try to Understand the Hierarchy between classes.
Use the project structure & directories to grasp what every package's purpose is.

- To run and test the project, you need to run application/application.py. That is the execution entry point.
  But first, there are a few things to do and understand (do not just bluntly run the app -it will mostly not work)
  
#### PRE-REQUISITES ####

- install libraries in requirements.txt (SQLAlchemy, SQLite). *(You may need a pip install or two on top of that)*

- In order for the project to run correctly, you need to install MySQL/MariaDB on your workstation
  You will also need a SQLite instance as well.
  You will find directions in the test files located in the test folder
  Make use of the Database Tool in PyCharm.
  
- The __init__.py file located in the repository folder is essential. 
  Its content is important and indispensable for comprehension. 
  You will see that, that is where the SQL engine switching logic takes place.

#### TODO ####

- When you're all set, and both your datbases and User tables are successfully tested, you may proceed to the application

- Create users, udpate them, play around with the API, switch SQL engines, and check/assert that the content of the User Tables changes accordingly.


