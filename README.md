# TLM Vehicle Routing Competition

Welcome to the TLM Vehicle Routing Competition, linked to Assignment 2 of the TLM course!

In this competition, you can earn bonus points by designing well-performing algorithms for the vehicle routing problem. All communication of this competition is via GitHub. If you have questions are comments related to the competition, please open an `Issue` in this GitHub repository.

## Making the code work

Steps from zero to hero (a submission):

0. [Make a GitHub account if you do not have this yet]
1. Clone this repository.
2. Make your own branch, called 'Group<>', with your group number between the brackets, e.g., 'Group1', all next steps assume you make adaptations to your own branch.
3. Make a new subfolder in the `Groups` folder, also called 'Group<>', so that the path to this folder is called `Groups/Group<>`. You can only work in this folder.
4. Copy the template code from the folder `GroupsTemplate` to your new folder
5. Have a look at the instruction in `main.py`, note that the file is by default set for running locally on your own PC. If you submit your code for the competition you will need to adapt your code according to the instructions.
6. As soon as you have programmed a working solution, you can submit your code to the leaderboard:
   1. Commit all your code
   2. Push your committed code to your own branch
   3. Make a Pull request (Best done on GitHub.com)

### Some remarks
* We recommend the use of PyCharm or Visual Studio Code, as those IDEs make the use of Git easier. But you can also use any other IDE using command line arguments for Git.
* We use the `VRPLIB` standard for instances and routes. So you have a standarized way to read instances and write solutions which you should follow.
* Instances are provided in the `Instances` folder.

## Competion rules and guidelines

1. You can only submit new code once per day, in order to limit computation times. The system checks this: A second submission on a day will result in ALL your submissions for that day to become invalid.
2. Please do not upload code with bugs.
3. You can only use the Python libraries listed in `main.py`, consult with us if you like to use other libraries.
4. We trust you to do your best to learn how to design well-performing algorithms by yourself, without cheating. Note that we will check the code of the winning group and some randomly selected groups
5. The competition consist of 2 rounds, with in each round a winning team.
6. Scores are determined based on the least distance (90% weight in round 1, 60% weight in round 2) and computational times (10% in round 1, 40% in round 2)
7. We limit the computational time to 5 minutes per day per group. If you did not find a solution within 5 minutes, your submission is invalid.
8. Only your best scoring solution is shown on the leaderboard. 
9. No rights can be derived from this information and the leaderboard at any moment in time.

## Compettion rewards

* The group that is first on the leaderboard in round 1 gets 0.25 bonus-points on Assignment 2
* The group that is first on the leaderboard in round 2 get 0.5 bonus-points on Assignment 2
* The winning groups present their approach (5 minutes) in the lecture after the competition ended.

# Provisional Leaderboard

No rights can be derived from below leaderboard, at the end of the competition the definite leaderboard will be published by us. Note that a lower score is better and that `Passed` indicates if your solution ran without bugs and finished within the timelimit of 5 minutes.

<!-- LEADERBOARD_START -->
| Rank | Date | GroupNumber | Passed | Score | Runtime |
| ------ | ------------ | ------------------- |-------------| ------- | ------- |
| 1 | 2024-02-02 | Group3 | ✅ | 44.23526008322155 | 0.00s |
| 2 | 2024-02-03 | Group14 | ✅ | 44.235294367813225 | 0.00s |
| 3 | 2024-02-02 | Group15 | ✅ | 44.235294367813225 | 0.00s |
| 4 | 2024-02-02 | Group13 | ✅ | 44.235294367813225 | 0.00s |
| 5 | 2024-02-02 | Group13 | ✅ | 44.235294367813225 | 0.00s |
| 6 | 2024-02-02 | Group11 | ✅ | 44.235294367813225 | 0.00s |
| 7 | 2024-02-02 | Group12 | ✅ | 44.235294367813225 | 0.00s |
| 8 | 2024-02-02 | Group1 | ❌ | 25.235294367813225 | 0.00s |
| 9 | 2024-02-02 | Group2 | ❌ | 44.23502801452394 | 0.01s |
<!-- LEADERBOARD_END -->