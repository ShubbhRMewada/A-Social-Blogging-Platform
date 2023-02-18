# IITM-Capstone_Project-Blog-Lite


<strong>Description:</strong>
  A multiuser social media-like web application for uploading blogs, photographs, and posts, among other things.
  Since this is a Multi-User Social Media Platform, 
  it should be capable of handling large volumes of data efficiently whilst also being aesthetically attractive. 
  It also needs to be concerned with the safety of the user's personally identifiable information.
  I have made every effort to bring them all into action.


<strong>Technologies used:</strong>
  
  For Front-End/User-Interface development: 
    HTML, CSS, Bootstrap:
      I used HTML for structure and CSS for design. 
      All of the elements, classes, and ids used in the ".html" file are given unique properties in a single ".css" file. 
      Bootstrap was employed to enhance the platform's appearance, interactivity, and functionality. 
      Bootstrap comes with features such as a sidebar, buttons, icons, and so forth.

    Jinja2:
      I'm pleased that we were able to employ this templating language. 
      It structured recurring needed parts such as the Sidebar for user engagement.
      The template inheritance feature of Jinja2 enabled the development of a specific interface design that should be consistent throughout the user's experience. 
      I've also used it to do basic database queries to prevent repeatedly displaying or forwarding data to the same ".html" file.
    
  For Back-End development:
      Python
      Flask
      Flask-Bcrypt -(For hashing sensitive user information before storing it in the database.)
      Flask-Login -(To optimize session management activities such as Log In and Log Out functionalities.)
      Flask-RESTful -(For creating REST APIs. 
                      This is analogous to the ORM mapping capabilities of Flask-SQLAlchemy, 
                      with the distinction that Flask-RESTful ORM must return values 
                      in JSON format based on the methods (POST, GET, PUT, DELETE) employed.)
      Flask-SQLAlchemy -(This is dominantly responsible for executing CRUD operations on the database using ORM capability.) 

  For Database Management:
      sqlite3
       
      
Core Functionalities of this Project:
    ── Login/Sign up page.
    ── User’s feed - posts, follow information etc.
    ── Users’s profile.
    ── Number of posts.
    ── Number of users following.
    ── Number of followers.
    ── Blog/Post management.
    ── Styling and Aesthetics.
    ── Proper login system.
    ── Exporting blog engagements.
    ── APIs for:
       ── User
       ── Blogs
       ── Others
    ── Validation on input fields.
    ── Blogs engagement.


Architecture and Features:

    ├───flaskblog (This package has all the important files like routing files(routes.py), ORM files(models.py), form files(forms.py) and (init.py) )
    │   │
    │   │───static (This folder saves all the Front-End development stuff including the “.css” file.)
    │   │   │
    │   │   ├───post_images (All the image files uploaded are stored here, which makes it easier to access.)
    │   │   │
    │   │   └───profile_pics (All the image files uploaded are stored here, which makes it easier to access.)
    │   │
    │   └───templates (All the “.html” pages are saved inside this folder.)
    │   
    │───run.py (This file is used to run initialise the localhost server and gets the app running and initialises the package named flaskblog.)
    │   
    │───api.py (This file is not a part of website development, it initialises the localhost server and waits for API method calls (POST, GET, PUT, DELETE).)
    │   
    │───requirements.txt (This file saves all packages and dependencies used while developing the project.)
    │   
    └───readme.txt (This file explains how to run the code.)
    

All the Core Functionalities are successfully implemented in this project. 
Some Additional functionality which I thought was important are :
    Reset Password link sent to the user  through Email using Flask-Mail -(For sending sensitive password reset mail to the user using SMTP.).
   

Find my Project Report here : https://docs.google.com/document/d/1dMIy1XSsfDwpAwJIHmzAD7EwSssffHZl/edit?usp=sharing&ouid=108888234288743889569&rtpof=true&sd=true
Find my Project PPT here : https://docs.google.com/presentation/d/1B6rXoLOc4RzQitUG6GF11s3cWpCjRUwbGM1FHoZif_Y/edit?usp=sharing
Find my Project Presentation Video here : https://drive.google.com/file/d/1RpFX4JspksDuwq6jGmt7f5SR-GM_jhHC/view?usp=sharing
Find my Published Collections API's for BLOG LITE here : https://documenter.getpostman.com/view/25129724/2s8Z6yYYg8


Thank you for your time; I hope you could observe my dedication and diligence throughout this massive endeavour.
