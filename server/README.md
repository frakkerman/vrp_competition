# Server side

All code was tested on a Linux (Ubuntu) server with command line interface. We recommend the use of MobaXterm or equivalent SSH client.

## Structure

* Competition_master: all main files used for pulling, evaluating and pushing results
  * Instances: the secret VRP instances used to evaluate the student code
  * logs: run logs written by the Cronjob
  * evaluate.py: the script that evaluates the student code
  * fetch.py: the script that fetches students repos from GitHub classroom
  * helper.py: some helpers used by evaluate.py
  * push.py: a script used to push the run results to a seperate leaderboard repo on GitHub
* Repos: place where we clone the student repos and write the results (see run_output)
## Setup

* Go through all Python files and make sure you understand them, change paths where needed.
* Upload all serve side files on your server
* Make a GitHub repo with the leaderboard
* Ensure the packages gh and gh-classroom are installed. Also make sure you have Python and all required libraries.
* We need a permanent connection to GitHub, so we can do this using a ssh keyfile
``ssh-keygen -t rsa -b 4096 -C "your_email@example.com"`` next:
 ``pbcopy < ~/.ssh/id_rsa.pub`` and test ``ssh -T git@github.com``
 * Now, you can pull the leaderboard repo
 * Finally, you need to setup a Cronjob which wil automatically run the required scripts, see an example below:
`` /usr/bin/python3 home_path/repos/clone_assignment_repos.py >> home_path/competition_master/logs/clone_$(date +\%Y-\%m-\%d_\%H-\%M).log 2>&1 && /usr/bin/python3 home_path/competition_master/evaluate.py >> home_path/competition_master/logs/eval_$(date +\%Y-\%m-\%d_\%H-\%M).log 2>&1 && /usr/bin/python3 home_path/competition_master/push.py >> /home/akkermanfr/competition_master/logs/push_$(date +\%Y-\%m-\%d_\%H-\%M).log 2>&1
``
This example Cronjob runs the 3 python files and writes all terminal output to a seperate logfile, which comes in handy if you encounter failures.
We ran the code each night at 24:00, this can be done using Cronjob.

## Troubleshooting

GitHub classroom can be a bit buggy, especially the automatic cloning sometimes fails when there are too many/too large student repos. 
Therefore, we have an additional way to download student repos. To do so, you need to go to the GitHub classroom and download the `gradelist.csv`, which lists all student repo names.
Next, you can use the `clone_assignment_repos.py` script in your Cronjob, instead of the `fetch.py` script. In principle you only need to download this csv file once, but keep it up-to-date when new groups join!
 
