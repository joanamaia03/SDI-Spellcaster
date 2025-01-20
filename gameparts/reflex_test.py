import random
import time

def perform_reflex_test():
    print("Get ready...")
    time.sleep(random.uniform(1, 3))
    print("GO!")
    start_time = time.time()
    input("Press Enter as fast as you can!")
    reaction_time = time.time() - start_time
    print(f"Your reaction time: {reaction_time:.3f} seconds")
    return reaction_time < 0.5  # Example threshold for successful defense