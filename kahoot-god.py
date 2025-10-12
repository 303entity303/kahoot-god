import requests
import json
import time
import gc
import argparse
import urllib3

urllib3.disable_warnings()

gc.disable()
parser = argparse.ArgumentParser()
parser.add_argument(
    "-v", "--verbose", action="store_true", help="Abilita il logging verboso"
)
args = parser.parse_args()
search_limit = 100
right_answers = []
auxiliary_array = []
aux_array_fake = ""
count = 0
question_count = 0
content_url = "https://create.kahoot.it/rest/kahoots/"
session = requests.Session()
session.get("https://create.kahoot.it/", timeout=0.7)
print("enter kahoot name:")
kahoot_name = input()
first_right_answer = int(input("Answer for question 1?"))
second_right_answer = int(input("Answer for question 2?"))
third_right_answer = int(input("Answer for question 3?"))
fourth_right_answer = int(input("Answer for question 4?"))
fifth_right_answer = int(input("Answer for question 5?"))
cursor = 0


def kahoot_found(Answers, kahoot_name):
    print("\n✅ quiz found")
    print(f"quiz name: {kahoot_name}")
    print("answers:")
    for i in range(len(Answers)):
        print(f"answer {i+1}: {Answers[i]}")
    session.close()
    quit()


try:
    start_time = time.time()
    while True:
        search_url = f"https://create.kahoot.it/rest/kahoots/?query={kahoot_name.replace(' ', '%20')}&cursor={cursor}&limit={search_limit}&orderBy=relevance"
        # print(f"\n🔎 Searching with cursor={cursor}...")
        response = session.get(search_url, timeout=2)
        # print("Status Code:", response.status_code)
        dati = response.json()
        if not dati.get("entities"):
            print(f"❌ No results at cursor={cursor}, stopping search.")
            break

        for entity in dati.get("entities", []):
            req_start = time.time()
            count += 1

            uuid = entity.get("card", {}).get("uuid")
            if not uuid:
                continue

            content_uuid = f"{content_url}{uuid}"

            try:
                content = session.get(content_uuid, timeout=(1, 1))
                content.raise_for_status()
                content = content.json()
                req_end = time.time()
                req_time = req_end - req_start
                total_time = req_end - start_time
                print(
                    f"Kahoot examined: {count} | request time: {req_time:.2f}s | total time: {total_time:.2f}s",
                    end="\r",
                    flush=True,
                )

            except Exception as e:
                print(f"⚠️ errore su {uuid}: {e}")
                continue

            current_kahoot_name = content.get("title", "Unknown")
            right_answers = []
            question_count = 0

            for question in content.get("questions", []):
                question_count += 1
                q_type = question.get("type")

                if q_type in ("content", "survey"):
                    continue

                elif q_type in ("quiz", "open_ended"):
                    for f, choice in enumerate(question.get("choices", [])):
                        if choice.get("correct"):
                            right_answers.append(f + 1)

                elif q_type == "slider":
                    right_answers.append(question.get("choiceRange", {}).get("correct"))

                elif q_type == "multiple_select_quiz":
                    aux_array_fake = " AND ".join(
                        c.get("answer", "")
                        for c in question.get("choices", [])
                        if c.get("correct")
                    )
                    right_answers.append(aux_array_fake)

                elif q_type == "jumble":
                    aux_array_fake = " ".join(
                        c.get("answer", "")
                        for c in question.get("choices", [])
                        if c.get("correct")
                    )
                    right_answers.append(aux_array_fake)

            if len(right_answers) >= 5:
                if (
                    right_answers[0] == first_right_answer
                    and right_answers[1] == second_right_answer
                    and right_answers[2] == third_right_answer
                    and right_answers[3] == fourth_right_answer
                    and right_answers[4] == fifth_right_answer
                ):
                    kahoot_found(right_answers, current_kahoot_name)

        # ✅ passa al batch successivo se non ha trovato niente
        cursor += 100
        # time.sleep(0.001)
except Exception as e:
    print(f"❌ error: {e}\ncontinuing anyway")
finally:
    session.close()
    print("session closed")
