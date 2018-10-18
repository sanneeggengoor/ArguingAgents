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
        [home_before_eating],
        after_dinner_michelin,
        {"quality":0.8, "low_price":0.1},
        "King orange goes to Michelin"
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

ac = [k_goes_to_michelin, k_goes_to_febo, t_goes_to_michelin, t_goes_to_febo]

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

valueset = ["quality", "low_price"]

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
    return State.propositions


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

def epistemic_reasoning(Init_state, Action):
    ## CQ 1
    if not Init_state == Q[0]:
        return False
    if not Init_state in rho(Action):
        return False
    return True



def choose_action(Init_state, Agent, goal):
    actions_agent = Agent.actions
    possible_actions = []
    for action in actions_agent:
        res_state = tau(Init_state, action)
        if problem_formulation(Init_state, res_state, action, goal):
            if epistemic_reasoning(Init_state, action):
                possible_actions.append(action)
    action_value_dict = {}
    for pos_action in possible_actions:
        action_value_dict[pos_action.name] = delta(pos_action)
    print("The possible actions with their values for this agent are:\t \t" + str(action_value_dict))
    return max(action_value_dict.items(), key=operator.itemgetter(1))[0]



# print("Set of states: \t" + str(Q))
# print("Initial State \t" + str(Q[0]))
# print("Set of Agents: \t"+ str(ag))
# print("Set of Actions of King Orange: \t"+ str(king_orange.actions))
# print("Set of Values of King Orange: \t"+ str(king_orange.values))
# print("Set of Propositions: \t"+str(phi))
# print("rho(k_goes_to_michelin):\t"+str(rho(k_goes_to_michelin)))
# print("tau(home_before_eating, k_goes_to_michelin):\t" +str(tau(home_before_eating, k_goes_to_michelin)))
# print("Delta functions:")
# print(Q)
# print(tau(home_before_eating,k_goes_to_michelin))

#

# print("Expected utility of Tokkie going to Michelin:\t \t" + str(delta(t_goes_to_michelin)))
# print("Expected utility of Tokkie going to Febo:\t \t" +str(delta(t_goes_to_febo)))
# print("Expected utility of King Orange going to Michelin:\t" +str(delta(k_goes_to_michelin)))
# print("Expected utility of King Orange going to Febo:\t \t" +str(delta(k_goes_to_febo)))
# print("pi(state home_before_eating): \t \t" + str(pi(home_before_eating)))
# print("Problem Formulation (home hungry to after_dinner_michelin with king to michelin and goal hungry true):\t \t" + str(problem_formulation(home_before_eating, after_dinner_michelin, k_goes_to_michelin, {"hungry": True})))
# print("epistemic_reasoning:\t \t" + str(epistemic_reasoning(home_before_eating,k_goes_to_michelin)))
print("Action that is chosen for agent King Orange who is hungry and home:\t \t" + str(choose_action(home_before_eating, king_orange, {"hungry":False})))
