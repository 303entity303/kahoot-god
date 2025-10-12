# Kahoot Finder

A simple Python script inspired by [kahoot-god](https://github.com/The-CodingSloth/kahoot-god).  
This version does **not use AI** — it asks the user for the Kahoot name and the correct answers for the first 5 questions, then searches for the correct Kahoot automatically.

---

## Installation and setup

- download it and run `pip install -r requirements.txt`, this will download everything the script needs
- done

---

## How to Use

1. Run the script with `python kahoot_god.py`
2. Enter the Kahoot name (first 2-3 words are enough) and press Enter.
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
Answer for question 1: 3
Answer for question 2: 1
Answer for question 3: 2
Answer for question 4: 4
Answer for question 5: 2
Searching for the correct Kahoot...
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
