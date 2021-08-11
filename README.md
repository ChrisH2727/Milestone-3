

<h1 align="center">Radioisotope Inventory Management</h1>

<span id="isotope"></span>

![Portfolio website](readmeimg/isotope.jpg)

A university physics faculty is required to maintain stock of radioactive sources for teaching and research purposes.

While individule radioactive sources do not pose a risk to health of students using them, collectively and in the wrong hands they could become a danger to the student community and security risk.

It is therefore crutial that the scientific staff contol student or accademic staff usage of these radioactive sources.

**[Access the application here.](https://isotope-3.herokuapp.com/)**

---

## Index 

- <a href="#ux">1. User experience (UX)</a>
  - <a href="#ux-goals">1.1. Project goals</a>
  - <a href="#ux-stories">1.2 User stories</a>
  - <a href="#ux-design">1.3 Design</a>
  - <a href="#info-architecture">1.4 Information architecture</a>
  - <a href="#wireframes">1.5 Wire Frames</a>
- <a href="#features">2. Features</a>
  - <a href="#features-existing">2.1 Features Implemented</a>
  - <a href="#features-future">2.2 Features for future implementation</a>
- <a href="#technologies-used">3. Technologies used</a>
- <a href="#testing">4. Testing</a>
- <a href="#deployment">5. Deployment</a>
- <a href="#credits">6. Credits</a>
- <a href="#acknowledgements">7. Acknowledgements</a>
- <a href="#disclaimer">8. Disclaimers</a>

---

<span id="ux"></span>

<h1>1. User experience (UX)</h1>

<span id="ux-goals"></span>

### 1.1 Project goals 

- Develop a full-stack application that allows users to access a common dataset.
- Develop a full-stack site that uses HTML, CSS, JavaScript, Python+Flask, MongoDB.

- Creat a website where students and accademic staff can:
    - register and be approved to use radioactive sources
    - see and select a radioactive source from a list of available radioactive sources and submit a request to use one.

- Create a website through which scientific staff can:
    - manage radioactive source allocation to students and accademic staff
    - Create Read Update and Delete radioactive source characteristic details
     
- Creating a website that is:
    - Simple to understand and easy to navigate
    - Presents different levels of access to information for students/accademics and scientific staff.

<span id="ux-stories"></span>

### 1.2 User stories

**First time user goals:**

1. As a first time user, I want to be able to register with the application so that I am authorised to use the radioactive sources available in the faculty.

**Existing user goals:** 
 
1. As a user, I want to login and out of the web application securely

2. As a user, I want to view my registration profil.

3. As a user, I want to change my password, department and research group.

4. As a user, I want to view all the sources that I have loaned so that I can determine which ones I need to return.

5. As a user, I want to search for different types of sources that I will need for my research work in the future and view the results.

6. As an user, I want the present activity of the source to be calculated and displayed so that I can confirm that it will be suitable for my work.

7. As a user, I want to create a request for a sources of the required type from the inventory of available sources and have my request approved.

8. As a user I want to delete my request prior to its approval if I change my mind regarding the type of source.

**Admin user goals:**

1. As an admin user, I want to approve user each registration request so that I can ensure that the correct Health and Safety briefing has been given.

2. As an admin user, I want to view the registration status of all other users.

3. As an admin user, I want to update the access rights of  other users to that of admin to create deputies

4. As an admin user, I want to suspend a user account to prevent a user from loaning more sources.

5. As an admin user, I want to permanently delete as user acccount, but only if the user has returned all loaned sources

6. As an admin user, I want to view the technical characteristices of all sources so that users can be advised on their selection.

7. As an admin user, I want to view the location of all sources on inventory to satisfy a security audit.

8. As an admin user, I want to create a new entry source entry with the same or different technical charateristc but with a unique serial number.

9. As an admin user, I want to update the technical characteristics of an existing source if there is an error either by selecting from the full inventory or by searching on the serial number.

10. As an admin user, I want to delete a source from the inventory either by selecting from the full inventory or by searching on the serial number, but only if that source has been returned to the inventory.

11. As an admin user, I want to view all the isotope types available

12. As an admin user I want to add isotope types and its respective half life to the list.

13. As an admin user I want to update information assocaited with an isotope.

14. As an admin user I want to delete isotope types, but only if all sources of that isotope type are not on loan.

15. As an admin user, I want to view the full history of source loans so that I can spot any patterns.

16. As an admin user, I want to view how many times a source has been loaned by isotope type so that I can dispose of sources that are not being loaned.

17. As an admin user, I want to view how user logins there have been on a given date so that I can assses how the service is being used.  

**Goals that would appeal to Scientists:**

1. As a scientist, I want to see information presented in a tabular form where possible so that I can spot patterns in the data.

**Goals that would appeal to the general user:** 

1. As a user or admin user, I may want to view information on small screen width devices which do not lend themselves to displaying data in tabular form.

2. As a user or admin user, I want to confirm any delete action that results in the permanet removal of information from the data base.

<span id="ux-design"></span>

### 1.3 Design 

- #### Colour scheme 

    The three colours that are used for the radioactive inventory website chosen not to detract from the important information that is presented.

    - **Light yellow** is used for the background to provide contrast for the blue **[Marterialize](https://materializecss.com/cards.html)** cards 

    - **Mid Blue** is used for the header and footer. 

    - **Light Blue** is used for the card panels and these are further inset with **white** cards panels to provide a heading for the page of section and to focus in on the form or table dispayed. 

- #### Fonts

    Sans serif and cursive are the fallbacks in case the main font isn’t being imported to the site correctly. 

- #### Icons

    In the project, icons are used that are provided by [Font Awesome](https://fontawesome.com/). The Icons that are used have functional purposes such as the hamburger menu and social media icons. 

- #### Images

    The images used are provided by [Shutterstock](https://www.shutterstock.com/).

- #### Tables

    As this website will predominently be utilised by individual from the scientific community, considerable use is made of tables. Scientists like to see information in tables so that they can see patterns of date.  **[Cloud Tables](https://cloudtables.com/)** provides an excelent free to use JQuery plugin for this purpose.

- #### Collapsibles

    Unfortunately tables do not render well on smaller screen devices and so use is made of the **[Collaspible](https://materializecss.com/collapsible.html)** provided by **Materialize**

<span id="info-architecture"></span>

### 1.4 Information architecture



TBD

<span id="wireframes"></span>

### 1.4 Wire Frames

TBD

<span id="features"></span>

## 2.0 Features

<span id="features-existing"></span>

 - Password - at least 8 characters of any type except spaces

 - email - must be in the form xxxxxxx@xxxxx.xxx

 - Research group - at least 3 characters no spaces hyphons and underscores permitted

### 2.1 Features implemented

- Users must first register to use the service and users accounts must be approved by an admin user.

- The application maintains a database of different radioactive sources with:
    - 

- Security

    - Password - at least 8 characters of any type except spaces

    - email - must be in the form xxxxxxx@xxxxx.xxx

    - Research group - at least 3 alphanumeric characters no spaces, hyphons and underscores permitted

    - Source serial number - at least 3 alphanumeric characters no spaces, hyphons and underscores permitted

    - Original activity - at least 2 numeric chacaters plus decimal point (?.?) only no white spaces   

    - half life - at least 2 numeric chacaters plus decimal point (?.?) only no white spaces

    - Isotopes - at least 1 uppercase alpha followed bt 1 lowercase alpha followed by 1 numeric digit - no decimal points or white spaces

    - Users are prevented from accessing html pages intended for admin users and are   

<span id="features-future"></span>

### 2.1 Features for furture implementation

- The current implementation is restricted to the creation, read, update and deletion of isotope types only. A future revision could be expanded to include more setting such as laboratory location and source encapsulation type.

- The current implementation does not include a calcuation for source dose. Future implementation could reference dose tables and provide this calculation.

- A future implementation could include the sending of emails to inform users that their accounts or requests sources have been approved 


<span id="technologies-used"></span>

<h1>3. Technologies used</h1>

- **Languages used**

    - [Python](https://www.python.org/)

        - Python provides backend functionality. The math module is used for asorted mathematical operations

    - [HTML5](https://en.wikipedia.org/wiki/HTML5)

        - HTML5 provides project structure and content for a browser to render.

    - [CSS3](https://en.wikipedia.org/wiki/Cascading_Style_Sheets)
    
        - CSS3 provides styling of the HTML5 elements.

    - [jQuery](https://jquery.com/)

        - jQuery used as the JavaScript functionality.

- **Frameworks, libraries & Plugins**

    - [Gitpod](https://www.gitpod.io/) 

        - The GitPod provides the development environment.

    - [Git](https://git-scm.com/)

        - The Git was used for version control to commit to Git and push to GitHub.

    - [GitHub](https://github.com/)

        - The GitHub is used as the project repository.

    - [Balsamiq](https://balsamiq.com/)

        - Balamiq is used to create wireframes.

    - [Materialize](https://materializecss.com/)

        - Materialize is used extensively for framework design.

    - [MongoDB](https://www.mongodb.com/1)
    
        -   MongoDB is the fully managed cloud database service used for the project.

    - [Heroku](https://dashboard.heroku.com/)

        - Heroki is the cloud platform used to deploy the service.

    - [Flask](https://flask.palletsprojects.com/en/1.1.x/)

        - Flask is the web framework used to provide libraries, tools and technologies for the app.

    - [Jinja](https://jinja.palletsprojects.com/en/2.11.x/)

        - Jinja is used for templating Python

    - [Werkzeug](https://werkzeug.palletsprojects.com/en/1.0.x/)

        - Werkzeug is used for password hashing.

    - [Cloud Tables](https://cloudtables.com/)

        - Used to generate the tables that are rendered

    - [Matplotlib](https://matplotlib.org/)

        - Python libraries used to generate histograms

- **Testing tools used** 

    - [Chrome DevTools](https://developers.google.com/web/tools/chrome-devtools/open) is used to detect problems and test responsiveness.

    -  [Autoprefixer](https://autoprefixer.github.io/)

        - Autoprefixer is used to parse the CSS and to add vendor prefixes to CSS rules.

    - [W3C Markup Validation Service](https://validator.w3.org/)

        - The W3C Markup Validation Service is used to check whether there were any errors in the HTML5 code.

    - [W3C CSS validator](https://jigsaw.w3.org/css-validator/)

        - The W3C CSS validator is used to check whether there were any errors in the CSS3 code.

    - [JShint](https://jshint.com/)

        - JShint is a JavaScript validator that is used to check whether there were any errors in the JavaScript code. 

    - [PEP8](http://pep8online.com/)

        - The PEP8 validator is used to check whether there were any errors in the Python code.

   <span id="testing"></span>

<h1>4. Test Approach</h1>

Functional testing will be based on <a href="#ux-stories"> 1.2 User stories</a>. The associated test methods, expected outcomes, tested outcomes and results are documented in document [TEST.md](TEST.md)

Non functional testing will be based on the non functional requirements set out in section 5.0

<span id="deployment"></span>

<h1>5. Deployment</h1>

**To be included**


<span id="credits"></span>

<h1>6. Credits </h1>

**Sources and Radioactive isotopes**

- Basic list of common radioactive isotopes form [Wikipedia](https://en.wikipedia.org/wiki/Radionuclide)

**Media**

- Login page image [Shutterstock](https://www.shutterstock.com/).

**Code**

- [Materialize](https://materializecss.com) for html code examples for: 
    
    - Collapsible
    
    - Navbar
    
    - Side navbar
    
    - Footer
    
    - Date picker

    - Text input

    - Radio button

    - 

- [Cloudtables](https://datatables.net/examples/) html and jQuery examples for the construction of tables that paginate

- Regex pattern for [email verification](https://ihateregex.io) 
Author's Github:https://github.com/geongeorge/i-hate-regex

- Handling 404 and 500 errors https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/

<span id="acknowledgements"></span>

<h1>7. Acknowledgements </h1>



<span id="disclaimer"></span>

<h1>8. Disclaimer </h1>

While the requirements for this project are based on an actual requirement, for security reasons, the information regarding radioactive sources is fictitious