# Kahoot Finder

A simple Python script inspired by [kahoot-god](https://github.com/The-CodingSloth/kahoot-god).  by @The-CodingSloth
This version does **not use AI** — it asks the user for the Kahoot name and the correct answers for the first 5 questions, then searches for the correct Kahoot automatically.

---

## Installation and setup

- download it and run `pip install -r requirements.txt`, this will download everything the script needs
- done

---

## How to Use

1. Run the script with `python kahoot_god.py`
2. Enter the Kahoot name (first 2-3 words are enough, more = faster but more chance of typing incorrectly) and press Enter.
3. Enter the correct answers for the first 5 questions, one at a time.<br/>
For example, if the answers are 1 2 3 4 1:
```
1 [Enter]
2 [Enter]
3 [Enter]
4 [Enter]
1 [Enter]
```
The script will then search for the Kahoot that matches your input.<br/>
```
$ python kahoot_god.py
enter kahoot name: Science Quiz
what's the right answer to question number 1?: 3
what's the right answer to question number 2?: 1
what's the right answer to question number 3?: 2
what's the right answer to question number 4?: 4
what's the right answer to question number 5?: 2
kahoots checked: xx
quiz name: Science Quiz 2025 Edition
answers:
answer 1: 3
answer 2: 1
answer 3: 2
answer 4: 4
answer 5: 2
answer 6: 1
answer 7: 4
answer 8: 2
answer 9: 3
answer 10: 1
```
