User Guide
==========

In this guide, users can find a detailed explanation of how to use the website.

Home Page
---------

This is the landing page of Readvice. Here, users can see the navigation bar at the top,
and top 10 books rated by the registereed users.
Using the navigation bar, users can navigate to the
books page where all the books are shown,
search for a book by name, go to register or login pages.
After logging in, "Sign up" and "Log in" buttons are replaced by "<username>",
which redirects to user's profile and "Log out" buttons.
If a user with admin privileges logs in, "Add Book" button is shown next to "Books" button.
It is important to note that the navigation bar is available in every page of the website
and it works the same way everywhere.

   .. figure:: images/Homepage.png
      :scale: 50 %
      :alt: Home page

      Home page of Readvice.

Registration Page
-----------------

This page provides a registration form that visitors can use to register to Readvice.
There are 6 fields on the registration form:
username, email, password, confirm password, gender and profile picture.
The first four fields are mandatory, while gender and profile picture fields are optional.
Username and email fields must be unique, and password fields have to match.
Some other constraints for these fields are:

Username should be between 3 and 20 characters.

Password should be between 6 and 32 characters.

Profile picture should be a .png, .jpg, .jpeg or .gif file.

If all the fields meet the requirements provided above,
registration completes succesfully,
and users are redirected to the home page and
they don't have to log in again.
Otherwise, registration page is reloaded with an appropriate error message.

   .. figure:: images/Register.png
      :scale: 50 %
      :alt: Registration page

      Registration page of Readvice.

Login Page
----------

This page provides a basic login form that visitors can use to log in to Readvice.
There are 3 fields on the login form: username, password and "Remember me".
If the information provided by the visitor is accurate,
they are successfully logged in and redirected to the home page.
Otherwise, they are shown an error in the login page
stating that they have entered invalid credentials.
If they check the "Remember me" checkbox, their user session will be kept
after the user closes their browser and they won't have to login again on their next visit.

   .. figure:: images/Login.png
      :scale: 50 %
      :alt: Login page

      Login page of Readvice.

Books Page
----------

This is where all the books in the database are listed.
Users can see the cover image, name and year information for books.
"Edit" and "Delete" buttons are provided for the admins at the bottom of each book.
Clicking on a book's name will redirect the user to that specific book's page.
In order to prevent longer load times, the books are divided into pages
that display 12 books at a time. Users can navigate through pages using
"Prev" and "Next" buttons available on the top right.

   .. figure:: images/Books.png
      :scale: 50 %
      :alt: Books page

      Books page of Readvice.

Book Page
---------

Detailed information about a certain book can be seen here.
On the left side, cover image of the book is shown.
In the middle, the following information about the book are provided in a table:
title, average score, author, publication year, genres and number of pages.
Title field will always be visible, but other fields are optional
and may not be shown if they are not provided.
Score field is only shown when there's at least 1 review for that book.
If the user is an admin, they can also see the "Edit" and "Delete" buttons.
On the right side, a summary of the book is displayed, if provided.

   .. figure:: images/Book.png
      :scale: 50 %
      :alt: Book page

      Book page of Readvice.

Below them, reviews for that book are shown. Reviews are ordered by date.
Each review section includes the user's, profile picture, username, score,
creation date for the review and a comment. Comments can be empty.
If there is no review yet, reviews field is not visible.
On the right side of each review, "Edit" and "Delete" butons are shown for appropriate users.
For example, every user can see these buttons next to their reviews but not other users'.
Admins can delete any review, but only edit their own reviews.

   .. figure:: images/Reviews.png
      :scale: 50 %
      :alt: Reviews section

      Reviews section of a book page.

Below reviews, "Write a review" section is available.
If the user is not logged in, they are prompted to register or login in order to write a review.

   .. figure:: images/WriteReviewNoLogin.png
      :scale: 50 %
      :alt: Write review no login

      Write a review section for unauthorized users.

Authorized users can see a review form, which has a score selection field and a comment field.
By default, 1 is selected for score. Comment field is optional.
Maximum length for comments is 2000 characters.
After submitting the review, user is redirected to the book's page,
and they can see their review at the bottom of reviews list.

   .. figure:: images/WriteReview.png
      :scale: 50 %
      :alt: Write review

      Write a review section for authorized users.

Search Page
-----------

Search page shows the list of books filtered by a certain criteria.
Otherwise, it is very similar to books page in terms of visuals.
This page can be accessed in two different ways:
By entering an input to the search box provided in the navigation bar
to search by title, or clicking on a book's year or genre fields to
filter the books based on that criteria. For example;
clicking on "2003" given in a book's year field
will show the books published in 2003.

   .. figure:: images/SearchQuery.png
      :scale: 50 %
      :alt: Search query

      Search results for a query.

   .. figure:: images/SearchYear.png
      :scale: 50 %
      :alt: Search year

      Books filtered by year.

Author Page
-----------

This page contains information about an author.
Authors are automatically generated after adding a book written by that author.
It can be accessed by clicking on the author's name in a book's page.
At the top, author's name is shown. Next to the name,
"Edit author" and "Delete author" buttons are shown for admins.
Below the name, the author's photo is shown.
To the right, information about the author is displayed.
Below that, books written by that author are listed.

   .. figure:: images/Author.png
      :scale: 50 %
      :alt: Author page

      Author page of Readvice.

Profile Page
------------

This page contains information about a certain user.
It can be accessed in two ways: Authorized users can access their own profile
by clicking on their name on the top right, or
clicking on a username in reviews section will redirect to that user's profile.
Profile pages display the user's username and an icon indicating
the user's gender if provided. Next to the name, users can see
"Edit" and "Delete" buttons in their own profile. "Delete" and "Make Admin"
buttons are visible to admins on all profiles. Clicking on the "Make Admin"
button will give that user admin privileges and turn it into a "Revoke Admin" button.
Below these, the user's profile picture is shown.
If the user has a profile picture, "Delete Profile Picture" button is provided below it.
Next to the profile picture, reviews written by that user are shown.

   .. figure:: images/Profile.png
      :scale: 50 %
      :alt: Profile page

      Profile page of a user.

Add Book / Edit Book Pages
--------------------------

Admins can access these pages in order to add a new book or edit an existing book.
They look identical, but Edit Book page will have its field filled with previous data.
Genres should be listed by putting a comma and a space between them.

   .. figure:: images/AddBook.png
      :scale: 50 %
      :alt: Add book page

      Add book page of Readvice.

Edit Profile Page
-----------------

This page is almost identical to registration page.
Users can change their username, email, password, gender or profile picture.
If password and profile picture fields are left empty, they won't be affected.
All the constraints described in registration section are valid here as well.

Edit Review Page
----------------

Users can edit their reviews by clicking on the "Edit" button at the right of their review.
This page is identical to the review form provided in book page.
Fields are filled with existing information.

Edit Author Page
----------------

Since authors are created automatically after adding a book of that author,
the only information they have is the name.
Admins can edit information about an author using this page.
3 fields are shown: Name, author photo and description.

   .. figure:: images/EditAuthor.png
      :scale: 50 %
      :alt: Edit author page

      Edit author page of Readvice.
