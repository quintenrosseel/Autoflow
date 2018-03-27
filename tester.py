from autoflow import *

# coloring1 = Coloring(coloring = {
#         Face("north"): Color.Green,
#         Face("east"): Color.Red,
#         Face("south"): Color.Green,
#         Face("west"): Color.Red})
#
# coloring2 = Coloring(coloring = {
#         Face("north"): Color.Red,
#         Face("east"): Color.Green,
#         Face("south"): Color.Red,
#         Face("west"): Color.Green})
#
# congestion1 = Congestion(congestion = {
#         Face("north"): Load(1),
#         Face("east"): Load(2),
#         Face("south"): Load(3),
#         Face("west"): Load(4)})
#
# congestion2 = Congestion(congestion = {
#     Face("north"): Load(5),
#     Face("east"): Load(6),
#     Face("south"): Load(7),
#     Face("west"): Load(8)})
#
# state1 = State(coloring1, congestion1)
#
# state2 = State(coloring2, congestion2)
#
# #assert state1 == state2, "State Structural Equality Error"
# #assert coloring1 == coloring2, "Coloring Structural Equality Error"
# #assert congestion1 == congestion2, "Congestion Structural Equality Error"
#
# action1 = Action(coloring1.coloring)
# action2 = Action(coloring2.coloring)
#
# quality = Quality()
#
# quality.add_state(state1)
# quality.add_state(state2)
# quality.add_action(state1, action1)
# quality.add_action(state1, action2)
# quality.add_action(state2, action1)
# quality.add_action(state2, action2)
# quality.add_performance(state1, action1, 100)
# quality.add_performance(state1, action2, 200)
# quality.add_performance(state2, action1, 300)
# quality.add_performance(state2, action2, 400)
#
# quality2 = Quality()
#
# quality2.add_state(state1)
#
# print(quality2)
#
# learner = Learner(state1)
# print(learner.state)
# learner.update(Face("north"), Load(20))
# learner.choose()
# print(learner.state)



# Simulation

coloring3 = Coloring(coloring = {
    Face("v"): Color.Red,
    Face("h"): Color.Green })

congestion3 = Congestion(congestion = {
    Face("v"): Load(0),
    Face("h"): Load(0) })

import random

rounds = 500
iters = 100

total_avg = 0
total_changed = 0
state3 = State(coloring3, congestion3)
learner3 = Learner(state3)
for j in range(0, rounds):

    learner3.state = deepcopy(state3)
    learner3.next = deepcopy(state3)

    changed = 0
    avg = 0

    for i in range(0, iters):
        # Change load
        for face in learner3.state.coloring:
            if i >= iters * 0.5:
                avg += learner3.avg_load()

            color = learner3.state.coloring[face]
            load = learner3.state.congestion[face]
            if color == Color.Green:
                learner3.update_load(face, Load(max(0, load.load - random.randint(1,10))))
            else:
                if face == Face("v"):
                    learner3.update_load(face, Load(load.load + random.randint(1,10)))
                else:
                    learner3.update_load(face, Load(load.load + random.randint(0,1)))

        # Choose new coloring
        if i > 0 and i % 5 == 0:
            coloring = learner3.state.coloring
            learner3.choose()
            if coloring != learner3.state.coloring:
                changed += 1

        # total += learner3.avg_load()
        # print(i,
        #       "v:", learner3.next.coloring[Face("v")][0], learner3.next.congestion[Face("v")],
        #       "h:", learner3.next.coloring[Face("h")][0], learner3.next.congestion[Face("h")],
        #       learner3.avg_load())
    total_changed += changed
    total_avg += avg / (iters * 0.5)
    print(avg / (iters * 0.5), learner3.count(), changed, sep="\t")
    # learner3.print()


print()
print(total_avg / rounds)
print(total_changed / rounds)
learner3.print()

