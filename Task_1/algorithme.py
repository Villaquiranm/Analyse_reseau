# -*- coding: utf-8 -*-

import random
import simpy
import matplotlib.pyplot as plt
from scipy.stats import sem, t
from scipy import mean
import numpy as np

confidence = 0.95
number_messages = 0
times = []
messages = []

def arrival(env,alpha, queue):
    global number_messages, times, messages
    times.append(0)
    messages.append(0)
    while True:
        yield env.timeout(random.expovariate(alpha))
        yield queue.put(1);
        number_messages = number_messages + 1
        times.append(env.now)
        messages.append(number_messages)
        print("Arrival : number of messages: ", number_messages,"[", env.now,"]")
        
        
def depart(env,lamda,queue):
    global number_messages, times, messages
    while True:
        yield queue.get()
        yield env.timeout(random.expovariate(lamda))
        number_messages = number_messages - 1
        times.append(env.now)
        messages.append(number_messages)
        print("Depart : number of messages: ", number_messages,"[", env.now,"]")
        
        
random.seed(random.uniform(1,100))
env = simpy.Environment()
pipe = simpy.Store(env, 10)

env.process(arrival(env, 15, pipe))
env.process(depart(env, 20, pipe))
env.run(until=50)

n = len(messages)
m = mean(messages)
std_err = sem(messages)
h = std_err * t.ppf((1 + confidence) / 2, n - 1)

start = m - h
end = m + h

n, bins, patches = plt.hist(x=messages, bins='auto', color='#0504aa',
                            alpha=0.7, rwidth=0.85)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Number of messages')
plt.text(23, 45, r'$\mu=15, b=3$')
maxfreq = n.max()
# Set a clean upper y-axis limit.
plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)

fig1, ax1 = plt.subplots()
ax1.step(times, messages);
ax1.set_ylabel('Number of messages')
ax1.set_xlabel('Time')

print ("Lower interval : ", start)
print ("Upper interval : ", end)
print ("Mean : ", m)