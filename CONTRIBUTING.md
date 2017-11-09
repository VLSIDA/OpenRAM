We are happy to accept contributions to OpenRAM and encourage this!
This document will let you know our preferred methodology for
including your contributions.

If you are unsure about a contribution, please email our development
list at openram-dev-group@ucsc.edu. We are happy to give insights into
the best way to implement a change to ensure your contribution will be
accepted and help other OpenRAM users.

# Code Style

Our code may not be the best and we acknowledge that. We welcome 
suggested changes to our coding style, but we also encourage users
to follow our styles so that OpenRAM remains a cohesive codebase.

# Testing

The most important consideration is that your changes should not break
other OpenRAM features. Please see the README.md file on how to run
the unit tests. Unit tests should work in all technologies. We will run
the tests on your contributions before they will be accepted.

# Pull Request Process

1. One time, create a GitHub account at http://github.com
2. Create a fork of the OpenRAM project on the github web page:
   https://github.com/mguthaus/OpenRAM
   It is on the upper right and says "Fork": This will make your own
   OpenRAM repository on GitHub in your account.
3. Clone your repository (or use an existing cloned copy if you've
   already done this once):
```
  git clone https://github.com/<youruser>/OpenRAM.git
  cd OpenRAM
```
4. Set up a new upstream that points to MY OpenRAM repository that you
   forked (only first time):
```
   git remote add upstream https://github.com/mguthaus/OpenRAM.git
```
   You now have two remotes for this project:
   * origin which points to your GitHub fork of the project. You can read
     and write to this remote.
   * upstream which points to the main project's GitHub repository. You can
     only read from this remote.
   You can remove remotes with
```
  git remote remove upstream
```
   if you previously added the one with the git@github that required
   authentication.
5. Make your own branch. The number one rule is to put each piece of
   work on its own branch:
```
  git checkout -b useful-branch-name
```
   Note that this is shorthand for:
```
  git branch useful-branch-name
  git checkout useful-branch-name
```
  "master" is the name of the branch that is the release version of the
  code (in your fork of the repository). You can check out the released
  code with "git checkout master" or go back to your ranch with
  "gitcheckout useful-branch-name".
6. Edit your code and make commits like normal:
```
  git add <new files>
  <edit files>
  git commit -m "Useful comment" <files changed>
```
   OR (sparingly, to commit all changes):
```
  git status
  <check that all the changed files are correct and should be commited>
  git commit -a -m "Useful comment"
```
   Run the unit tests entirely. Fix all bugs.
7. After you are done (or while you are editing and you see changes in
   MY master branch) make sure you have the most recent from MY master
   and merge any changes. Pull the updated copy from MY master branch in
   MY repository:
```
 git pull upstream master
```
  This is important because we may have had other updates that conflict
  with your changes and you must resolve them with current state of
  master (the released, working code). You may have to merge changes if
  they overlap your changes, so do this often to avoid the problem. You
  now need to push this to the master of YOUR forked repository as well:
```
 git push origin master
```
  if you are on your master branch. Otherwise, just git push.
8. Push your branch to YOUR repository:
```
 git push -u origin useful-branch-name
```
   Remember origin is your copy on github and useful-branch-name is the
   branch that you made to contain all your changes.
   The -u flag links this branch with the remote one, so that in the
   future, you can simply type git push origin.
9. When you are done, go to GitHub and you will see a button to notify
   me.  Press the button and it will notify me of your pushed branch.
   This will have you fill in a form for the contribution that gets sent
   to me.
10. I will review the request and may have you fix stuff if the tests
    don't pass, you didn't merge all my changes in master from other
    contributions, or your style of code is bad.
11. Go back to step 3 for your next contribution. Remember, you can
    push/pull work to your repository all the time and can pull from my
    master as well. Make sure to add large features so that You don't have
    to add lots of pull requests.
