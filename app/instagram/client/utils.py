from random import randint
import time

def sleep(lb=80, ub=130):
  seconds = randint(lb, ub) / 10
  time.sleep(seconds)

def validate_tags(tags):
    if isinstance(tags, list):
        if len(tags) == 0:
            print("Must have at least one tag")
            return

        print(
            "Tags only support one value for now. Setting first tag as the selected"
        )
        return tags[0]

def gen_count(session, for_follow=True):
    # follow less if following is greater
    ratio = session.ff_ratio
    
    counts = randint()
    return counts