We are happy to accept contributions to OpenRAM and encourage this!
This document will let you know our preferred methodology for
including your contributions.

If you are unsure about a contribution, please email our development
list at openram-dev-group@ucsc.edu. We are happy to give insights into
the best way to implement a change to ensure your contribution will be
accepted and help other OpenRAM users.

# Directory Structure

* compiler - openram compiler itself (pointed to by OPENRAM_HOME)
  * compiler/base - base data structure modules
  * compiler/pgates - parameterized cells (e.g. logic gates)
  * compiler/bitcells - various bitcell styles
  * compiler/modules - high-level modules (e.g. decoders, etc.)
  * compiler/verify - DRC and LVS verification wrappers
  * compiler/characterizer - timing characterization code
  * compiler/gdsMill - GDSII reader/writer
  * compiler/router - router for signals and power supplies
  * compiler/tests - unit tests
* technology - openram technology directory (pointed to by OPENRAM_TECH)
  * technology/freepdk45 - example configuration library for [FreePDK45 technology node
  * technology/scn4m_subm - example configuration library [SCMOS] technology node
  * technology/scn3me_subm - unsupported configuration (not enough metal layers)
  * technology/setup_scripts - setup scripts to customize your PDKs and OpenRAM technologies
* docs - LaTeX manual (outdated)
* lib - IP library of pregenerated memories

# Code Style

Our code may not be the best and we acknowledge that. We welcome 
suggested changes to our coding style, but we also encourage users
to follow our styles so that OpenRAM remains a cohesive codebase.

# Testing

The most important consideration is that your changes should not break
other OpenRAM features. Please see the README.md file on how to run
the unit tests. Unit tests should work in all technologies. We will run
the tests on your contributions before they will be accepted.

# Internal Development

For internal development, follow all of the following steps EXCEPT
do not fork your own copy. Instead, create a branch in our private repository
and consult with me when you want to merge it into the dev branch.
All unit tests should pass first.

# Pull Request Process

1. One time, create a GitHub account at http://github.com

2. Create a fork of the OpenRAM project on the github web page:
   https://github.com/vlsida/openram
   It is on the upper right and says "Fork": This will make your own
   OpenRAM repository on GitHub in your account.

3. Clone your repository (or use an existing cloned copy if you've
   already done this once):
```
  git clone https://github.com/<youruser>/oepnram.git
  cd openram
```

4. Set up a new upstream that points to MY OpenRAM repository that you
   forked (only first time):
```
   git remote add upstream https://github.com/vlsida/openram.git
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

5. Start with dev:
```
 git checkout dev
```
  "dev" is the name of the branch that 
  is the development version. You should submit all contributions as changes
  to the dev branch. "master" is the name of the branch that is the release version of the
  code (in your fork of the repository). You can check out the released
  code with "git checkout master”. 

6. Make your own branch from dev. The number one rule is to put each piece of
   work on its own branch:
```
  git checkout -b useful-branch-name
```
   Note that this is shorthand for:
```
  git branch useful-branch-name
  git checkout useful-branch-name
```

7. Edit your code and make commits:
```
  <edit files>
  git add <new files>
  git commit -m "Useful comment" <files changed>
```
   OR (sparingly, to commit all changes):
```
  git status
  <check that all the changed files are correct and should be committed>
  git commit -a -m "Useful comment"
```
   Run the unit tests entirely. Fix all bugs.

8. After you are done (or while you are editing and you see changes in
   MY dev branch) make sure you have the most recent from MY dev
   and merge any changes. Pull the updated copy from MY master dev in
   MY repository:
```
 git pull upstream dev
```

9. Frequently rebase your branch to keep track of current changes in dev. 
```
 git fetch upstream
 git rebase origin/dev
```

10. After a final rebase and your code is working, push your branch to YOUR repository:
```
 git push -u origin useful-branch-name
```
   Remember origin is your copy on github and useful-branch-name is the
   branch that you made to contain all your changes.
   The -u flag links this branch with the remote one, so that in the
   future, you can simply type git push origin. Do not rebase after you push 
   the branch!

11. When you are done, go to GitHub and you will see a button to notify
   me.  Press the button and it will notify me of your pushed branch.
   This will have you fill in a form for the contribution that gets sent
   to me.

12. I will review the request and may have you fix stuff if the tests
    don't pass, you didn't merge all my changes in dev from other
    contributions, or your style of code is bad.

13. Go back to step 3 for your next contribution. Remember, you can
    push/pull work to your repository all the time and can pull from my
    dev as well. Make sure to add large features so that You don't have
    to add lots of pull requests.
