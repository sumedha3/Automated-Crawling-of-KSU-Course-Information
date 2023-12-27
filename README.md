# Automated-Crawling-of-KSU-Course-Information

## Application Technical Flow:
In our project once the application is up and running, we see the below home page:

<img width="572" alt="image" src="https://github.com/sumedha3/Automated-Crawling-of-KSU-Course-Information/assets/112127474/49c5e7dd-09d1-4159-8ee5-51cb2f28c1fd">

So, from the figure you can see that we have few operations where a student can use them to register, enroll, check for registered coursed and some suggestions for next course registrations.
The route which we can see on browser when we get this home page is ‘http://127.0.0.1:5000/home’.
Once the user is clicking on the register button from the nav bar on the home page, he will be redirected to the registration page. As any user who is using the application needs to register first then the user can login, enroll and check the classes registered.
The registration page looks like:

<img width="590" alt="image" src="https://github.com/sumedha3/Automated-Crawling-of-KSU-Course-Information/assets/112127474/1615b395-990a-4ea9-94ff-5edd7e141329">

Fields which we have mentioned in the registration page are required fields by which we are asking the user to differentiate their own account.
Email ID is taken as a primary field here, as a user can register only with one unique email id.
Password is to make them login into their own account which we are matching from database with the corresponding mail id. Here the password is stored in encrypted format in our database where no one can steal it till the user is sharing it.
First and Last names are taken just to see their personal details and to verify their personal details.
We are taking their education level just to check their level of education and suggest the courses they can take in the next semester.
Once the data is given correctly on the application the data will be directly stored in the database in the below format.

<img width="486" alt="image" src="https://github.com/sumedha3/Automated-Crawling-of-KSU-Course-Information/assets/112127474/2e12931e-bd5a-4b15-9e6e-fae22ec6e18f">

Here the password is stored in encrypted format for security reasons. 
From now on users can login into the application to enroll in the courses.

<img width="828" alt="Screen Shot 2023-12-27 at 5 05 54 PM" src="https://github.com/sumedha3/Automated-Crawling-of-KSU-Course-Information/assets/112127474/814c14c3-6d50-46aa-8643-f9a3927c86f9">

When the user landing to enrollment page he/she need to select the department and course to which they are enrolling to.
Here department doesn’t give any filter to the course list, it is just to get information from user so that we can recommend the course in their suggestions.
Once they click on the enroll button the selected course will be added into their classes. And the classes tab look like:

<img width="830" alt="Screen Shot 2023-12-27 at 5 08 47 PM" src="https://github.com/sumedha3/Automated-Crawling-of-KSU-Course-Information/assets/112127474/8822b801-de57-4de6-994e-8ed45208a512">

Here the user can see his/her courses into which they have enrolled. They can see all the details about the course like code, title, description, credits, and term into which they have enrolled.
Now coming to course suggestions, we are taking the courses which have already registered by the used and suggesting other courses which they can take in the next semester.

The suggestion which we designed look like:

<img width="826" alt="Screen Shot 2023-12-27 at 5 10 35 PM" src="https://github.com/sumedha3/Automated-Crawling-of-KSU-Course-Information/assets/112127474/e790ccf3-c793-43de-9f33-e500d81d5ee2">

So, from the above snapshot we can see the user is already registered in CS 57206 and CS 690699. For the course CS 57206 we have some suggestions with course codes CS 57221 and CS 63015. But there are no suggestions for the course CS 690699 as it is a capstone project.





