To upload an existing repository to GitHub, you will first need to create a new repository on GitHub. Once you have created the repository, you can use the following steps to push your local repository to the GitHub repository:

Open a terminal window and navigate to the local repository that you want to upload.
Initialize the repository as a Git repository by running the command git init
Add the GitHub repository as a remote to your local repository by running the command git remote add origin [GitHub repository URL]. This URL can be copied from the GitHub repository page.
Add all of the files in your local repository to the staging area by running the command git add .
Commit the files with a message by running the command git commit -m "Initial commit"
Push the files to the GitHub repository by running the command git push -u origin master. The -u flag sets the origin remote as the default for future pushes.
Note: Make sure you have git installed on your system and you have the correct URL of your github repo.


Gitignore
 To ignore the files/folders in the current commit you need to remove them first by using git rm -r --cached folder_name and then commit the changes.


 You can remove individual files from the staging area by using the git reset command followed by the file name.
 git reset file.txt
git rm --cached -r myProject/__pycache__
git rm --cached -r myProject/client/__pycache__
git rm --cached -r myProject/translator/__pycache__



…or push an existing repository from the command line
git remote add origin https://github.com/sdplatt/m1cro.git
git branch -M main
git push -u origin main

Branch 'main' set up to track remote branch 'main' from 'origin'.

https://github.com/sdplatt/m1cro

#regular updates
git push -u origin main

#heroku should work automatically
https://m1cro6.herokuapp.com/