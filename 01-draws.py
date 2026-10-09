import collections
import time

from silicon import *

persona = "You are a woman in your thirties who lives in the Midwest of the United States and finished high school."
question = "If the election for the United States House of Representatives were held today, would you vote for the Democratic candidate, the Republican candidate, someone else, or would you not vote? How confident are you, from 0 to 100?"

for model in MODELS + EXTRA_MODELS:
    votes = []
    for i in range(20):
        start = time.time()
        votes.append(ask(model, persona, question, temperature=1.0, draw=i)["vote"])
        print(f"  {model} draw {i + 1}/20 ({time.time() - start:.1f}s)", flush=True)
    print(model, collections.Counter(votes))
print(f"Spent ${total_spent():.4f}")
