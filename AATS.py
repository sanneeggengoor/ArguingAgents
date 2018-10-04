'''FORMAL AATS'''


class State:
    def __init__(self,
                propositions):
        self.propositions = propositions

class Action:
    def __init__(self,
                initial_states,
                resulting_state,
                utilities):
        self.initial_states = initial_states
        self.resulting_state = resulting_state
        self.utilities = utilities

class Agent:
    def __init__(self,
                actions,
                values):
        self.actions = actions
        self.values = values



#### STATES

home_before_eating = State(
        {"hungry": True}            #dictionary with propositions (from Phi)
)
after_dinner_michelin = State(
        {"hungry": False}
)
after_dinner_febo = State(
        {"hungry": False}
)

# finite, non-empty set of states with the first item as initial state
Q = [home_before_eating,
    after_dinner_michelin,
    after_dinner_febo]

#### ACTIONS

k_goes_to_michelin = Action(
        [home_before_eating],
        after_dinner_michelin,
        {"quality":0.8, "low_price":0.1}
)
k_goes_to_febo = Action(
        [home_before_eating],
        after_dinner_febo,
        {"quality":0.2, "low_price":0.9}
)

t_goes_to_michelin = Action(
        [home_before_eating],
        after_dinner_michelin,
        {"quality":0.8, "low_price":0.1}
)
t_goes_to_febo = Action(
        [home_before_eating],
        after_dinner_febo,
        {"quality":0.2, "low_price":0.9}
)



#### AGENTS

king_orange = Agent(
        [k_goes_to_michelin, k_goes_to_febo],   #list with actions
        {"quality":0.9, "low_price":0.1}        #dictionary with values
)

tokkie = Agent(
        [t_goes_to_michelin, t_goes_to_febo],
        {"quality":0.3, "low_price":0.8}
)
# finite, non-empty set of agents
ag = [king_orange, tokkie]


# finite, non-empty set of atomic propositions (things like: hungry, home etc., these could both be true or false)
# Phi = [prop1, prop2, prop3]
phi = ["hungry"]

# # finite, non-empty set of values for each agent
# # Av1 = {val1a: ...., val1b: ..., val1c: ...}
# Av_king_orange = king_orange.values

# print(tokkie.values)

# will return the set of states from which every action in ActionSet may be executed
def rho(Action):
    return Action.initial_states


# will return state that would result from JointAction in state State
def tau(State, Action):
    if (State in Action.initial_states):
        return Action.resulting_state
    else:
        print("Error: this action (" + Action + ") is not allowed from State ("+ State +")")



# will return the set of primitive propositions satisfied in each case
def pi(State):
    propositions = State.propositions
    proplist = []
    for item in phi:
        if propositions.get(item):
            proplist.append(item)
    return proplist

# print(pi(home_before_eating))

def get_involved_agent(Action):
    for agent in ag:
        if Action in agent.actions:
            return agent

def delta(Action):
    involved_agent = get_involved_agent(Action)
    values = involved_agent.values
    utilities = Action.utilities
    exp_ut = 0
    for item in values:
        exp_ut += utilities[item] * values[item]
    return exp_ut






print(delta(t_goes_to_michelin))
print(delta(t_goes_to_febo))
print(delta(k_goes_to_michelin))
print(delta(k_goes_to_febo))



### make function to get involved agent instead of having it defined in class Action.
