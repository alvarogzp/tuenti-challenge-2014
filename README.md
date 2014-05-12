[Tuenti Challenge](https://contest.tuenti.net/) 4 (2014)
=========================

This are my solutions of the Tuenti Challenge 4 (2014 edition), and the scripts used to submit them.



Solutions
---------

I successfully completed the first 13 challenges.

For each challenge, you'll find:
- The file with the code that solves the challenge, with the extension according to the language used.
- The challenge input and output for the test and submit phase.
- In some challenges, there are some extras.

What you won't find:
- The challenge description, you can find it on https://contest.tuenti.net/Challenges
- Any challenge-specific file provided in the description (they tend to be very huge).


### Some challenge notes

While doing challenge 10, I discovered the index.py of challenge 18 and decompiled it, so I have also put it here.

I am aware of the stack overflow in challenge 4, I have maintained it because that was the way I submitted it.



Test & submit scripts
---------------------

The included test_challenge and submit_challenge scripts are a modified version of the [original ones](https://contest.tuenti.net/Info/tools) to dump the input and output of the challenge to a file, in order to inspect it later.

They also print some useful information while running: the execution time of the code and the URIs requested with the time to request them.

