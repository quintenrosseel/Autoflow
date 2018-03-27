from copy import deepcopy
import random
import math

class Simulation:

    def __init__(self,
                 learner,
                 initial_state,
                 rounds,
                 steps,
                 display=True,
                 choice_frequency=5,
                 heavy_faces=None,
                 depart_range=(1,10),
                 heavy_range=(1,10),
                 light_range=(0,1)
                 ):

        self.learner = learner
        self.initial_state = initial_state
        self.rounds = rounds
        self.steps = steps
        self.display = display
        self.choice_frequency = choice_frequency
        self.heavy_faces = heavy_faces
        self.depart_range = depart_range
        self.heavy_range = heavy_range
        self.light_range = light_range

    def run(self):
        total_avg = 0
        total_changed = 0

        for j in range(0, self.rounds):

            self.learner.state = deepcopy(self.initial_state)
            self.learner.next = deepcopy(self.initial_state)

            changed = 0
            avg = 0

            for i in range(0, self.steps):
                for face in self.learner.state.coloring:

                    if i >= self.steps * 0.5:
                        avg += self.learner.avg_load()

                    color = self.learner.state.coloring[face]
                    load = self.learner.state.congestion[face]

                    if color == Color.Green:
                        self.learner.update_load(
                            face,
                            Load(max(0, load.load - random.randint(*self.depart_range))))
                    else:
                        if face in self.heavy_faces:
                            self.learner.update_load(
                                face,
                                Load(load.load + random.randint(*self.heavy_range)))
                        else:
                            self.learner.update_load(
                                face,
                                Load(load.load + random.randint(*self.light_range)))

                if i > 0 and i % self.choice_frequency == 0:
                    coloring = self.learner.state.coloring
                    self.learner.choose()
                    if coloring != self.learner.state.coloring:
                        changed += 1

            total_changed += changed
            total_avg += avg / (self.steps * 0.5)

        all_load = total_avg / self.rounds
        all_change = total_changed / self.rounds
        if self.display:
            print("Load:", all_load, sep="\t")
            print("Change:", all_change, sep="\t")

        return all_load, all_change


class Learner:
    """ (Reinforcement) Learner

        Args:
            initial_state: State object to start with
    """
    a = 0.1
    g = 0.9
    t = 0.1

    def __init__(self, initial_state, policy="q", reward=10):
        self.state = deepcopy(initial_state)
        self.next = deepcopy(initial_state)
        self.reward_value = reward
        self.policy = policy

        self.q = Quality()
        self.q.add_state(initial_state)

    def choose(self):
        """ choose an action, update the q-value and next -> state """

        if not self.q.has_state(self.state):
            self.q.add_state(self.state)

        if self.policy == "q":
            action_choice = self.q_switch()
        else:
            action_choice = self.naive_switch()

        old = self.q[self.state][action_choice]
        rew = self.reward(self.state)
        self.next.update_coloring(action_choice.as_dict())

        if not self.q.has_state(self.next):
            self.q.add_state(self.next)
        opt = self.optimal(self.next)

        new_q = (1-self.a) * old + self.a * (rew + self.g * opt)
        self.q[self.state][action_choice] = new_q

        self.state = deepcopy(self.next)
        return action_choice

    def reward(self, state):
        """ Get the reward corresponding to the current state """

        return self.reward_value if state.avg_load() == 0 else 0

    def optimal(self, state):
        """ Get the maximum possible q-value for this state from """

        best = 0
        for action in self.q[state]:
            best = max(best, self.q[state][action])
        return best

    def update_load(self, face, load):
        """ update the current load at a face """

        self.next.update_load(face, load)

    def naive_switch(self):
        """ Return the action of a different coloring than the current """

        return list(filter(lambda a:
                           a != Action(self.state.coloring.as_dict()),
                           self.q.get_actions(self.state).keys()))[0]

    def q_switch(self):
        """ Return the action according to Q SoftMax """

        r = random.random()
        actions = self.q.get_actions(self.state)
        total = sum(map(lambda a: math.pow(math.e, actions[a]), actions))
        acc = 0
        for action in actions:
            acc += math.pow(math.e, actions[action]) / total
            if r <= acc:
                return action

    def avg_load(self):
        """ Get the current average load of all the faces """

        return self.next.avg_load()

    def print(self):
        """ Print all state-actions with a nonzero q-value """

        for state in self.q.q:
            for action in self.q.q[state]:
                if self.q.q[state][action] > 0:
                    print(repr(state),
                          repr(action),
                          self.q.q[state][action],
                          sep="\t" )

    def count(self):
        """ Count the number of state-actions with a nonzero q-value """

        total = 0
        for state in self.q.q:
            for action in self.q.q[state]:
                if self.q.q[state][action] > 0:
                    total += 1
        return total


class Quality:
    """ Quality of choosing a certain action at a certain state
        Map from State -> Action -> Performance Measure """

    def __init__(self):
        self.q = {}

    def has_state(self, state):
        return state in self.q

    def add_state(self, state):
        self.q[deepcopy(state)] = {action:0
                                   for action in state.possible_actions()}

    def add_action(self, state, action):
        self.q[state][action] = 0

    def add_performance(self, state, action, performance):
        self.q[state][action] = performance

    def get_actions(self, state):
        return self.q[state]

    def __str__(self):
        return "Quality(\n" + \
               "\n".join([repr(state) + "\t->\t" +
                          repr(action) + "\t->\t" +
                          repr(self.q[state][action])
                   for state in self.q
                   for action in self.q[state]]) + "\n)"

    def avg_load(self):
        return self.next.avg_load()

    def __getitem__(self, item):
        return self.q[item]


class Action:
    """ Represents to what color the traffic lights will turn
        Map of Faces of an intersection to their corresponding Color

        Args:
            action: Map[Face,Color]
    """
    def __init__(self, action):
        self.action = action

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(frozenset(self.action))

    def __str__(self):
        return "Action(\n" + \
               "\n".join(["\t" + str(face) + "\t->\t" + str(self.action[face])
                          for face in self.action]) + ")"

    def __repr__(self):
        return "".join([repr(face) + repr(self.action[face])
                        for face in self.action])

    def as_dict(self):
        return self.action


class State:
    """ Represents the current state of an intersection

    Args:
        coloring: Coloring
        congestion: Congestion
    """
    def __init__(self, coloring, congestion):
        self.coloring = coloring
        self.congestion = congestion

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash((self.coloring.__hash__(),
                     self.congestion.__hash__()))

    def __str__(self):
        return "State(" \
               + str(self.coloring) + "," \
               + str(self.congestion) + ")"

    def __repr__(self):
        return "".join([repr(face) +
                        repr(self.coloring[face]) +
                        repr(self.congestion[face])
                        for face in self.coloring])

    def is_empty(self):
        return all([load == Empty for load in self.congestion])

    def possible_actions(self):
        return [Action(self.coloring.as_dict()),
                Action(self.coloring.switch())]

    def update_load(self, face, load):
        self.congestion.update(face, load)

    def update_coloring(self, action):
        self.coloring = Coloring(coloring = action)

    def avg_load(self):
        return self.congestion.avg_load()


class Coloring:
    """ Represents what the traffic lights are currently colored
        Map of Faces of an intersection to their corresponding Color

        Args:
            faces(optional): initialize each face with Color.Off
            coloring(optional): provide a Map[Face,Color]
    """

    def __init__(self, faces = None, **coloring):
        if faces is not None:
            self.coloring = {face:Color.Off for face in faces}
        else:
            self.coloring = coloring['coloring']

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(frozenset(self.coloring))

    def __str__(self):
        return "Coloring(" + \
               ",".join([str(face) + ":" + str(self.coloring[face])
                          for face in self.coloring]) + ")"

    def __repr__(self):
        return "".join([repr(face) + repr(self.coloring[face])
                        for face in self.coloring])

    def __iter__(self):
        return self.coloring.__iter__()

    def __getitem__(self, item):
        return self.coloring[item]

    def as_dict(self):
        return self.coloring

    def switch(self):
        return {face : Color.Green
                if self.coloring[face] == Color.Red
                else Color.Red
                for face in self.coloring}


class Color:
    """ Domain of colors for a traffic light """
    Green = "g"
    Red = "r"
    Off = "o"


class Face:
    """ Inputs to an intersection

        Args:
            face: identifier for face of intersection
    """
    def __init__(self, face):
        self.face = face

    def __eq__(self, other):
        return self.face == other.face

    def __hash__(self):
        return self.face.__hash__()

    def __str__(self):
        return "Face(" + str(self.face) + ")"

    def __repr__(self):
        return repr(self.face)


class Congestion:
    """ Map of Faces of an intersection to their corresponding Load

        Args:
            faces(optional): initialize each face with Empty
            congestion(optional): provide a Map[Face,Load]
    """
    def __init__(self, faces = None, **congestion):
        if faces is not None:
            self.congestion = {face: Empty for face in faces}
        else:
            self.congestion = congestion['congestion']

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(frozenset(self.congestion))

    def __str__(self):
        return "Congestion(" + \
               ",".join([str(face) + ":" + str(self.congestion[face])
                          for face in self.congestion]) + ")"

    def __repr__(self):
        return "".join([repr(face) + repr(self.congestion[face])
                        for face in self.congestion])

    def __iter__(self):
        return self.congestion.__iter__()

    def __getitem__(self, item):
        return self.congestion[item]

    def update(self, face, load):
        self.congestion[face] = load

    def avg_load(self):
        return sum(map(lambda c:
                       self.congestion[c].load, self.congestion)) \
               / len(self.congestion)


class Load:
    """ Abstract amount of pressure/load at a face of the intersection

        Attributes:
            load (int): quantity of load
    """
    def __init__(self, load):
        self.load = load

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return "Load(" + str(self.load) + ")"

    def __repr__(self):
        return repr(self.load)

    def __add__(self, other):
        return self.load + other


""" Special Loads """
Empty = Load(0)
