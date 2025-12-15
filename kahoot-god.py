import requests
import json
import time
import gc
import subprocess
import argparse
import urllib3
import os
check_ver_url=("https://github.com/303entity303/kahoot-god/"
    "releases/latest/download/kahoot-god.py"
)
__VERSION__ = "1.2.1"
def check_version():
    try:
        response = requests.get(check_ver_url, timeout=3)
        print(response.status_code)
        if response.status_code == 200:
            for line in response.text.splitlines():
                if line.startswith("__VERSION__"):
                    print(line)
                    latest_version = line.split('=')[1].strip().strip('"').strip("'")
                    if latest_version != __VERSION__:
                        print(f"⚠️ A new version ({latest_version}) is available. You are using version {__VERSION__}. Please update.")
                        update_choice = input("Do you want to update now? (y/n):")
                        print(f"test {update_choice.strip().lower()}")
                        
                        if update_choice.strip().lower() == 'y':
                            print("Updating...")
                            python_executable = os.sys.executable
                            script_path = "updater.py"
                            subprocess.Popen([python_executable, script_path])
                            print("Updater started. Exiting current instance.")
                            os._exit(0)
                    return
    except:
        pass
check_version()
urllib3.disable_warnings()
gc.disable()
parser = argparse.ArgumentParser()
parser.add_argument("-d","--debos", action="store_true", help="Don't use this i made it so i can quickly find kahoot from one of my profssors")
args = parser.parse_args()
search_limit = 100
right_answers = []
auxiliary_array = []
aux_array_fake = ""
count = 0
question_count = 0
content_url = "https://create.kahoot.it/rest/kahoots/"
session = requests.Session()
session.get("https://create.kahoot.it/", timeout=0.4)
print("enter kahoot name:")
kahoot_name = input()
ProvidedRightAnswers = []
if not args.debos:
    for i in range(5):
        ProvidedRightAnswers.append(input(f"what's the right answer to question number {i+1}?"))

cursor = 0

def kahoot_found(Answers, kahoot_name):
    print("\n✅ quiz found")
    print(f"quiz name: {kahoot_name}")
    print("answers:")
    for i in range(len(Answers)):
        print(f"answer {i+1}: {Answers[i]}")
    quit()
try:
    start_time = time.time()

    while True:
        if args.debos:
            search_url = f"https://kahoot.it/rest/kahoots/?query=debos73&cursor={cursor}&limit={search_limit}&creator=debos73"
        else:
            search_url = f"https://kahoot.it/rest/kahoots/?query={kahoot_name.replace(' ', '%20')}&cursor={cursor}&limit={search_limit}&orderBy=relevance"
        #print(f"\n🔎 Searching with cursor={cursor}...")
        response = session.get(search_url, timeout=5, verify=False)
        
        #print("Status Code:", response.status_code)
        dati = response.json()
        if not dati.get("entities"):
            #print(f"❌ No results at cursor={cursor}, stopping search.")
            break

        for entity in dati.get("entities", []):
            req_start = time.time()
            count += 1

            uuid = entity.get("card", {}).get("uuid")
            if not uuid:
                continue

            content_uuid = f"{content_url}{uuid}"

            try:
                content = session.get(content_uuid, timeout=(1, 3))
                content.raise_for_status()
                content = content.json()
                req_end = time.time()
                req_time = req_end - req_start
                total_time = req_end - start_time
                print(f"kahoots checked: {count}", end="\r", flush=True)

            except Exception as e:
                #print(f"⚠️ errore su {uuid}: {e}")
                continue

            current_kahoot_name = content.get("title", "Unknown")
            right_answers = []
            question_count = 0

            for question in content.get("questions", []):
                question_count += 1
                q_type = question.get("type")

                if q_type in ("content", "survey"):
                    continue

                elif q_type == "quiz":
                    for f, choice in enumerate(question.get("choices", [])):
                        if choice.get("correct"):
                            right_answers.append(str(f + 1))
                            
                elif q_type == "open_ended":
                    right_answers.append(question.get("choices")[0]["answer"])

                elif q_type == "slider":
                    right_answers.append(str(question.get("choiceRange", {}).get("correct")))

                elif q_type == "multiple_select_quiz":
                    aux_array_fake = str(" AND ".join(
                        c.get("answer", "") for c in question.get("choices", []) if c.get("correct"))
                    )
                    right_answers.append(aux_array_fake)

                elif q_type == "jumble":
                    aux_array_fake = str("|".join(
                        c.get("answer", "") for c in question.get("choices", []) if (c.get("correct")) or not ((c.get("correct"))))
                    )
                    right_answers.append(aux_array_fake)
            #print(f"{current_kahoot_name} | {uuid}", end="\n")
            if len(right_answers) >= 5:
                if not args.debos:
                    if right_answers[:5] == ProvidedRightAnswers[:5] :
                        kahoot_found(right_answers, current_kahoot_name)
                elif kahoot_name.lower() in current_kahoot_name.lower():
                    kahoot_found(right_answers, current_kahoot_name)
        # ✅ passa al batch successivo se non ha trovato niente
        cursor += 100
        #time.sleep(0.3)
except Exception as e:
    print(f"{e}")


    quit()
