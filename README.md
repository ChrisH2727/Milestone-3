

<h1 align="center">Radioisotope Inventory Management</h1>

<span id="isotope"></span>

![Portfolio website](readmeimg/isotope.jpg)

A university physics faculty is required to maintain stock of radioactive sources for teaching and research purposes.

While individule radioactive sources do not pose a risk to health of students using them, collectively and in the wrong hands they could become a danger to the student community and security risk.

It is therefore crutial that the scientific staff contol student or accademic usage of these radioactive sources.

**[Access the application here.](https://isotope-3.herokuapp.com/)**

---

## Index 

- <a href="#ux">1. User experience (UX)</a>
  - <a href="#ux-goals">1.1. Project goals</a>
  - <a href="#ux-stories">1.2 User stories</a>
  - <a href="#ux-design">1.3 Design</a>
  - <a href="#ux-architecture">1.4 Information architecture</a>
  - <a href="#ux-mockup">1.5 Wire Frames</a>
- <a href="#features">2. Features</a>
  - <a href="#features-existing">2.1 Existing features</a>
  - <a href="#features-future">2.2 Features left to implement in the future</a>
- <a href="#technologies">3. Technologies used</a>
- <a href="#testing">4. Testing</a>
- <a href="#deployment">5. Deployment</a>
- <a href="#credits">6. Credits</a>
- <a href="#Acknowledge">7. Acknowledge</a>
- <a href="#Acknowledge">8. Disclaimer</a>

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

**First-time visitor goals:**
1. As a first time user, I want to be able to register with the application so that I am authorised to use the radioactive sources available in the faculty.


**User goals:** 
 
1. As a user I want to login and out of the web application securely
1. As a user, I want to view my profile. 
1. As a user, I want to be able to change my password, department and research group.
1. As a user, I want to view all that radioactive sources that I have on loan. 
1. As a user, I want to see the radioactive isotopes that are available to use and place a request to use one or more. 
1. As . 


**Admin goals:**

As an admin user I want all  --- 


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