<h1 align="center">Radioisotope Inventory Management</h1>
<h2 align="center"> Milestone 3 Project</h2>

<span id="isotope"></span>

## Index

- <a href="#nonfunctional-test">1. Non-functional test</a>
- <a href="#usecase-test">2. Use case (functional) test</a>
- <a href="#defects">3. Defects</a>

---
<h1>1. Non functional test</h1>

<span id="nonfuctional test"></span>

- **javascript static code analaysis**

    ![Jshint Report](testimg/Jshint_report.png)

    No errors or wanings reported.

- **CSS validation report**

    ![WC3 Validation Report](testimg/CSS_report.png)

    No errors or wanings reported.

- **HTML Validation Report**

    With the inclusion of the Jinja templating engine, it is not possible to paste html code into the validator. Instead the application is run and the browser tools used to expose the html source code. This is then pasted into the validator.

    |HTML Page |Errors |Warnings |
    |---|---|---|
    |Login| None | See comment below, |
    |Registration| None | See comment below |
    |User Profile| None | Checked with top and side navbar. See comment below|
    |Source Request| None | Checked with top and side navbar. See comment below|
    |Logout| None | Checked with top and side navbar. See comment below|
    |Approve Source Loan Request | None | Checked with top and side navbar. See comment below|
    |User Access Manangement| None | Checked with top and side navbar.|
    |Full Inventory Listing| None | Checked with top and side navbar.|
    |Update Source| None | Checked with top and side navbar.|

 - **Responsiveness Report**
 
    |HTML Page |1640px |ipadPro |ipad|iphone 5/SE|
    |---|---|---|---|---|
    |Login| |  |   |   |
    |Registration|  |
    |User Profile|  | |
    |Source Request|  | |
    |Logout|  | |
    |Approve Source Loan Request | Pass | Pass | Pass |Pass|
    |User Access Manangement| Pass | Pass | Pass |Pass|
    |Full Inventory Listing| Pass | Pass | Pass |Pass|
    |Update Sources| Pass | Pass | Pass |Pass|

 - **Navigation Report**
 
    |HTML Page |1640px |ipad|
    |---|---|---|
    |Login| |  |   |
    |Registration| |  |
    |User Profile|  | |
    |Source Request|  | |
    |Logout|  | |
    |Approve Source Loan Request | Pass | Pass |
    |User Access Manangement| Pass | Pass |
    |Full Inventory Listing| Pass | Pass |
    |Update Sources| Pass | Pass |
<h1>2. Use case (functional) test</h1>

<span id="usecase-test"></span>

1. As a first time user, I want to be able to register with the application so that I am authorised to use the radioactive sources available in the faculty.

    - **Test Method**

    - **Expected Outcome**

    - **Tested Outcome**

2. As a user, I want to login and out of the web application securely

    - **Test Method**

    - **Expected Outcome**

    - **Tested Outcome**

3. As a user, I want to view my registration profil.

    - **Test Method**

    - **Expected Outcome**

    - **Tested Outcome**

4. As a user, I want to change my password, department and research group.

    - **Test Method**

    - **Expected Outcome**

    - **Tested Outcome**

5. As a user, I want to view all the sources that I have loaned so that I can determine which ones I need to return.

    - **Test Method**

    - **Expected Outcome**

    - **Tested Outcome**

6. As a user, I want to search for different types of sources that I will need for my research work in the future and view the results.

    - **Test Method**

    - **Expected Outcome**

    - **Tested Outcome**

7. As an user, I want the present activity of the source to be calculated and displayed so that I can confirm that it will be suitable for my work.

    - **Test Method**

    - **Expected Outcome**

    - **Tested Outcome**

8. As a user, I want to create a request for a sources of the required type from the inventory of available sources and have my request approved.

    - **Test Method**

    - **Expected Outcome**

    - **Tested Outcome**

9. As a user I want to delete my request prior to its approval if I change my mind regarding the type of source.

    - **Test Method**

    - **Expected Outcome**

    - **Tested Outcome**

10. As an admin user, I want to approve user each registration request so that I can ensure that the correct Health and Safety briefing has been given.

    - **Test Method**

    - **Expected Outcome**

    - **Tested Outcome**

11. As an admin user, I want to view the registration status of all other users.

    - **Test Method**

    - **Expected Outcome**

    - **Tested Outcome**

12. As an admin user, I want to update the access rights of  other users to that of admin to create deputies

    - **Test Method**

    - **Expected Outcome**

    - **Tested Outcome**

13. As an admin user, I want to suspend a user account to prevent a user from loaning more sources.

    - **Test Method**

    - **Expected Outcome**

    - **Tested Outcome**

14. As an admin user, I want to permanently delete as user acccount, but only if the user has returned all loaned sources

    - **Test Method**

    - **Expected Outcome**

    - **Tested Outcome**

15. As an admin user, I want to view the technical characteristices of all sources so that users can be advised on their selection.

    - **Test Method**

    - **Expected Outcome**

    - **Tested Outcome**

16. As an admin user, I want to view the location of all sources on inventory to satisfy a security audit.

    - **Test Method**

    - **Expected Outcome**

    - **Tested Outcome**

17. As an admin user, I want to create a new entry source entry with the same or different technical charateristc but with a unique serial number.

    - **Test Method**

    - **Expected Outcome**

    - **Tested Outcome**

18. As an admin user, I want to update the technical characteristics of an existing source if there is an error either by selecting from the full inventory or by searching on the serial number.

    - **Test Method**

    - **Expected Outcome**

    - **Tested Outcome**

19. As an admin user, I want to delete a source from the inventory either by selecting from the full inventory or by searching on the serial number, but only if that source has been returned to the inventory.

    - **Test Method**

    - **Expected Outcome**

    - **Tested Outcome**

20. As an admin user, I want to view all the isotope types available

    - **Test Method**

    - **Expected Outcome**

    - **Tested Outcome**

21. As an admin user I want to add isotope types and its respective half life to the list.

    - **Test Method**

    - **Expected Outcome**

    - **Tested Outcome**

22. As an admin user I want to update information assocaited with an isotope.

    - **Test Method**

    - **Expected Outcome**

    - **Tested Outcome**

23. As an admin user I want to delete isotope types, but only if all sources of that isotope type are not on loan.

    - **Test Method**

    - **Expected Outcome**

    - **Tested Outcome**

24. As an admin user, I want to view the full history of source loans so that I can spot any patterns.

    - **Test Method**

    - **Expected Outcome**

    - **Tested Outcome**

25. As an admin user, I want to view how many times a source has been loaned by isotope type so that I can dispose of sources that are not being loaned.

    - **Test Method**

    - **Expected Outcome**

    - **Tested Outcome**

26. As an admin user, I want to view how user logins there have been on a given date so that I can assses how the service is being used.  

    - **Test Method**

    - **Expected Outcome**

    - **Tested Outcome**

27. As a scientist, I want to see information presented in a tabular form where possible so that I can spot patterns in the data.

    - **Test Method**

    - **Expected Outcome**

    - **Tested Outcome**

28. As a user or admin user, I may want to view information on small screen width devices which do not lend themselves to displaying data in tabular form.

    - **Test Method**

    - **Expected Outcome**

    - **Tested Outcome**

29. As a user or admin user, I want to confirm any delete action that results in the permanet removal of information from the data base.

    - **Test Method**

    - **Expected Outcome**

    - **Tested Outcome**


<h1>3. Defects</h1>

<span id="defects"></span>

|No|Defect Description |Defect resolution |
|---|----------------- |----------------- |
|1| "no source found flash message is displayed before user query's for aan available source|  |
|2|Clear isotope update button crashed program  |Re-direct code flow to use function "manage_isotopes" |
|3| Detect condition where the isotope halflife is required as the key to searching for an isotope to update but has been deleted| |
|4| Approve Source Loan Request Page has email address and not user name|Add python code to display user first name and last name |
|5|User management page had button colour mismatch between table and collapsible.|Add html code to give buttons same appearance| 