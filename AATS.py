'''FORMAL AATS'''

import operator

class State:
    def __init__(self,
                propositions):
        self.propositions = propositions

class Action:
    def __init__(self,
                initial_states,
                resulting_state,
                utilities,
                name):
        self.initial_states = initial_states
        self.resulting_state = resulting_state
        self.utilities = utilities
        self.name = name

class Agent:
    def __init__(self,
                actions,
                values):
        self.actions = actions
        self.values = values



#### STATES

home_before_eating = State(
        {"hungry": True},            #dictionary with propositions (from Phi)
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
        [home_before_eating],               # possible initial states
        after_dinner_michelin,              # following state
        {"quality":0.8, "low_price":0.1},   # utilities associated with this action
        "King orange goes to Michelin"      # name of the action
)
k_goes_to_febo = Action(
        [home_before_eating],
        after_dinner_febo,
        {"quality":0.2, "low_price":0.9},
        "King orange goes to FEBO"
)

t_goes_to_michelin = Action(
        [home_before_eating],
        after_dinner_michelin,
        {"quality":0.8, "low_price":0.1},
        "Tokkie goes to Michelin"
)
t_goes_to_febo = Action(
        [home_before_eating],
        after_dinner_febo,
        {"quality":0.2, "low_price":0.9},
        "Tokkie goes to FEBO"
)


# list of possible actions
ac = [k_goes_to_michelin, k_goes_to_febo, t_goes_to_michelin, t_goes_to_febo]

#### AGENTS

king_orange = Agent(
        [k_goes_to_michelin, k_goes_to_febo],   #list with actions agent can perform
        {"quality":0.9, "low_price":0.1}        #dictionary with values
)

tokkie = Agent(
        [t_goes_to_michelin, t_goes_to_febo],
        {"quality":0.3, "low_price":0.8}
)
# finite, non-empty set of agents
ag = [king_orange, tokkie]

valueset = ["quality", "low_price"]

# finite, non-empty set of atomic propositions (things like: hungry, home etc., these could both be true or false)
# Phi = [prop1, prop2, prop3]
phi = ["hungry"]


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
    return State.propositions



# returns the agent involved in this action
def get_involved_agent(Action):
    for agent in ag:
        if Action in agent.actions:
            return agent


# valuation function with expected utility
def delta(Action):
    involved_agent = get_involved_agent(Action)
    values = involved_agent.values
    utilities = Action.utilities
    exp_ut = 0
    for item in values:
        exp_ut += utilities[item] * values[item]
    return exp_ut

#stage 1 critical questions
def problem_formulation(Init_state,Resulting_state, Action, goal):
    involved_agent = get_involved_agent(Action)
    ## CQ 2
    if tau(Init_state, Action) != Resulting_state:
        return False
    ## CQ 3
    if not all(x in set(list(pi(Init_state).keys())) for x in set(list(goal.keys()))):
        return False
    ## CQ12
    if Init_state not in Q:
        return False
    ## CQ13
    if Action not in ac:
        return False
    ## CQ14
    if tau(Init_state, Action) not in Q:
        return False
    ## CQ 15
    if not all(x in set(valueset) for x in set(involved_agent.values.keys())):
        return False

    ## CQ 16
    for state in Q:
        if all(x in set(list(pi(state).keys())) for x in  set(list(goal.keys()))):
            for value in list(goal.keys()):
                if goal.get(value) != pi(state).get(value):
                    break
                return True
    return False

# stage2 epistemic reasoning
def epistemic_reasoning(Init_state, Action):
    ## CQ 1
    if not Init_state == Q[0]:
        return False
    if not Init_state in rho(Action):
        return False
    return True


# function to choose action
def choose_action(Init_state, Agent, goal):
    actions_agent = Agent.actions
    possible_actions = []
    # loop through all actions agent can perform
    for action in actions_agent:
        res_state = tau(Init_state, action)
        # make sure they pass the critical questions
        if problem_formulation(Init_state, res_state, action, goal):
            if epistemic_reasoning(Init_state, action):
                possible_actions.append(action)
    action_value_dict = {}
    # calculate expected utilities
    for pos_action in possible_actions:
        action_value_dict[pos_action.name] = delta(pos_action)
    print("The possible actions with their values for this agent are:\t \n" + str(action_value_dict))
    # return highest action
    return max(action_value_dict.items(), key=operator.itemgetter(1))[0]



print("Action that is chosen for agent King Orange who is hungry and home:\t \n" + str(choose_action(home_before_eating, king_orange, {"hungry":False})))
