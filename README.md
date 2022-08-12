<div align="center">

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![GUN 3.0 License][license-shield]][license-url]

</div>

## 📌 About The Project
This is a PR tool for sunbirddcim/test_automation.  
This project is aim to better PR management and faster/easier PR creation.

## 📌 Usage

- Create a new pull request
  1. Create a new branch for your PR (ex. `TMD-12345`).
  2. Click `New Pull Request` button.
  3. Click the upload area to upload the refine test test. (Note that your filename must match the corresponding branch name ex. `TMD-12345.txt`)
  4. For the first upload, you must fill the `Reviewers`, `Assignees` and `Labels`.
  5. Select the base branch
  6. Check the PR branch, title, body, reviewers, assignees and labels again.
  7. Click `Create Pull Request` button.

## [📌 Report a bug](https://github.com/Ming119/PR_Tool/issues)

- ### Please follow the below guidelines if you would like to report a bug:

  1. **Use the GitHub issue search** &mdash; check if the issue has already been reported.

  2. **Check if the issue has been fixed** &mdash; try to reproduce it using the latest `main` or development branch in the repository.

  3. **Isolate the problem** &mdash; create a [reduced test case](http://css-tricks.com/reduced-test-cases/) and a live example.


  Example:

  > Short and descriptive example bug report title
  >
  > A summary of the issue and the browser/OS environment in which it occurs. If
  > suitable, include the steps required to reproduce the bug.
  >
  > 1. This is the first step
  > 2. This is the second step
  > 3. Further steps, etc.
  >
  > `<url>` - a link to the reduced test case
  >
  > Any other information you want to share that is relevant to the issue being
  > reported. This might include the lines of code that you have identified as
  > causing the bug, and potential solutions (and your opinions on their
  > merits).

## [📌 Contribute](https://github.com/Ming119/PR_Tool/pulls)
-  ### Follow this process if you'd like your work considered for inclusion in the project
  1. [Fork](http://help.github.com/fork-a-repo/) the project, clone your fork, and configure the remotes:
  
      ```bash
      # Clone your fork of the repo into the current directory
      git clone https://github.com/Ming119/PR_Tool
      # Navigate to the newly cloned directory
      cd PR_Tool
      # Assign the original repo to a remote called "upstream"
      git remote add upstream https://github.com/Ming119/PR_Tool
      ```

  2. If you cloned a while ago, get the latest changes from upstream:
  
      ```bash
      git checkout <dev-branch>
      git pull upstream <dev-branch>
      ```
  
  3. Create a new topic branch (off the main project development branch) to contain your feature, change, or fix:

      ```bash
      git checkout -b <topic-branch-name>
      ```

  4. Locally merge (or rebase) the upstream development branch into your topic branch:

      ```bash
      git pull [--rebase] upstream <dev-branch>
      ```

  5. Push your topic branch up to your fork:

      ```bash
      git push origin <topic-branch-name>
      ```
  6. [Open a Pull Request](https://help.github.com/articles/using-pull-requests/) with a clear title and description.

  >  **IMPORTANT**: By submitting a patch, you agree to allow us to license your work under the same license as that used by `PR_Tool`

[contributors-shield]: https://img.shields.io/github/contributors/Ming119/PR_Tool.svg?style=for-the-badge
[contributors-url]: https://github.com/Ming119/PR_Tool/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Ming119/PR_Tool.svg?style=for-the-badge
[forks-url]: https://github.com/Ming119/PR_Tool/network/members
[stars-shield]: https://img.shields.io/github/stars/Ming119/PR_Tool.svg?style=for-the-badge
[stars-url]: https://github.com/Ming119/PR_Tool/stargazers
[issues-shield]: https://img.shields.io/github/issues/Ming119/PR_Tool.svg?style=for-the-badge
[issues-url]: https://github.com/Ming119/PR_Tool/issues
[license-shield]: https://img.shields.io/github/license/Ming119/PR_Tool?label=license&style=for-the-badge
[license-url]: https://github.com/Ming119/PR_Tool/blob/main/LICENSE
