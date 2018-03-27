from autoflow import *

initial_coloring = Coloring(coloring = {
    Face("v"): Color.Red,
    Face("h"): Color.Green })

initial_congestion = Congestion(congestion = {
    Face("v"): Load(0),
    Face("h"): Load(0)})

initial_state = State(initial_coloring, initial_congestion)

learner = Learner(initial_state, policy="q")

sim = Simulation(learner,
                 initial_state,
                 rounds = 500,
                 steps = 100,
                 heavy_faces = [Face("v")],
                 depart_range=(1,10),
                 heavy_range=(1,10),
                 light_range=(0,1))

for i in range(0,20):
    sim.run()
