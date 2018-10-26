# -*- coding: utf-8 -*-
"""

"""
class Agent:
    # initializing the agent, including its values, states and actions
    def __init__(self,
                 values,
                 states,
                 all_actions={}):
        # values is a dictionary containing the personal values of the agent.
        self.values = values
        """
        states is a dictionary containing elements of the "state"-class. Each
        element is an element of the state with a "current" and a "desired"
        state. The "current" state of the agent can be described as the sum of
        the "current" values of all elements of the state-class.
        """
        self.states = states
        """
        All actions are all actions an agent can take. This is a dictionary
        with entries for all actions. These entries at the moment have each a
        list consisting of two dictionaries: The first is the state-changes
        that follow from acting out the action,. The second are the parameters
        that are used to calculate the utility of the action for the agent.
        """
        self.all_actions = all_actions


    # Adding a new dictionary of values to the existing values.
    # Careful: Existing values will be overwritten!
    def update_values(self, new_values):
        self.values.update(new_values)

    # Making the agent act based on current state, including change in state.
    # It also gives output with information of all steps.
    def act(self):
        
        """ Functions used inside act """
        
        """
        Returning the "current state" of the agent as well as the "desired
        state" by looping through all state-items belonging to the agent. 
        Whether a state-item will be part of the desired state depends on
        whether the current state is above a certain threshold. This threshold
        defines the point at which the agent feels like the current state is
        so unsatisfying that a change towards the desired state is necessary.
        """
        def curr_state():
            current_state_dict = {} # Contains all attributes of current state
            current_state_prints = [] # Contains info to print curr_state
            desired_state = {} # Contains all attributes of desired state
            # Looping through all state-elements
            for i in self.states:
                state = self.states[i]
                # Checking whether element is above threshold
                if state.current >= state.threshold:
                    # State of element set to "True", as its above threshold
                    current_state_dict[i] = True
                    current_state_prints.append([i, state.current])
                    # Element added to desired state
                    desired_state[i] = state.desired
                else:
                    current_state_dict[i] = False
                    current_state_prints.append([i, state.current])
            return current_state_dict, current_state_prints, desired_state
                    
        """
        Purely testing what actions are possible from the current state, 
        regardless of whether these are at all desirable for the agent.
        """
        def curr_poss_act(current_state_dict):
            curr_actions = []
            for i in self.all_actions:
                for j in self.all_actions[i].possible_states:
                    if j == current_state_dict:
                        curr_actions.append(i)
            return curr_actions
        
        """
        Taking possible actions and desired state, computing which actions
        lead to the most desirable new state. All actions that satisfy this
        requirement are returned.
        """
        def curr_des_act(actions, desired_state):
            curr_actions = {} # Holding the actions' names and "meters"
            # Looping through all possible actions
            for i in actions:
                target_meter = 0 # Tracks "desiredness" for each action
                # Looping through state-elements of desired state
                for j in desired_state:
                    """
                    For each element of the desired state, it is checked
                    whether a change in this direction is represented in the
                    action. The closer the change brings the new state to the
                    desired state, the higher this will be valued. Ultimately,
                    this is represented in the target meter. This 
                    desiredness-value is also multiplied by the factor in the
                    value system of the agent, as changes in different states
                    might be differently important to the agent.
                    """
                    if j in self.all_actions[i].state_changes:
                        action_state_changes = self.all_actions[i].state_changes[j]
                        change = self.all_actions[i].state_change_function(self.states[j].current, 
                                                 action_state_changes[0], 
                                                 action_state_changes[1])
                        change_factor = self.states[j].current - change / self.states[j].current - desired_state[j]
                        target_meter += change_factor * self.values[j]
                if len(curr_actions) > 0:
                    if curr_actions["meter"] == target_meter:
                        curr_actions["actions"].append(i)
                    elif curr_actions["meter"] < target_meter:
                        curr_actions["meter"] = target_meter
                        curr_actions["actions"] = [i]
                else:
                    curr_actions["meter"] = target_meter
                    curr_actions["actions"] = [i]
            return curr_actions["actions"]                        

        """
        Of all "selected actions" leading to equally desirable new states, the 
        utilities regarding the "secondary properties" is done and returned in
        a sorted manner. This is about "how" the new state is reached, not
        how desirable the state itself is.
        """
        def val_function(curr_actions):
            utility_list = []
            for i in curr_actions:
                utility = 0
                curr_action_probabilities = self.all_actions[i].attributes
                for j in curr_action_probabilities:
                    utility += curr_action_probabilities[j] * self.values[j]
                utility_list.append([utility, i])
            return sorted(utility_list, reverse=True)

        """ Beginning of the "actual" function "act" """

        # Getting current state, printing it
        current_state_dict, current_state_prints, desired_state = curr_state()
        print("Current State: " + str(current_state_prints))
        
        # Calculating all possible actions from the current state
        curr_actions = curr_poss_act(current_state_dict)
        print("Possible Actions: " + str(curr_actions))
        
        # Calculating actions that lead to new state closest to desired state
        curr_actions = curr_des_act(curr_actions, desired_state)
        print("Actions with most desired states: " + str(curr_actions))

        # Calculating utilities of those actions
        curr_utilities = val_function(curr_actions)
        print("Utilities of actions: ")
        for i in curr_utilities:
            print(str(i[1]) + ": " + str(i[0]))

        # Showing best action!
        chosen_action = curr_utilities[0]
        print("Chosen action by agent: " + chosen_action[1])

        # Updating current state
        ca_statchange = self.all_actions[chosen_action[1]].state_changes
        """
        Looping through all changes in the current state. The change also
        depends on which function is used to change the state(see below)
        """
        for i in ca_statchange:
            changes = ca_statchange[i]
            self.states[i].current = self.all_actions[chosen_action[1]].state_change_function(self.states[i].current,
                       changes[0], changes[1])
        current_state_dict, current_state_prints, desired_state = curr_state()
        print("New State: " + str(current_state_prints))

"""
The Action-class is a class of all actions that an agent can in principle take.
"""
class Action:
    def __init__(self,
                 state_changes = {},
                 attributes = {}, 
                 possible_states = []):
        """
        State changes contains a dictionary with all changes that happen when
        the action is acted out. Each changed state-attribute is represented
        by its name and a list with both the numeric value for the change and
        the name of the change function as a string(see below).
        This looks like:
            {"name_of_state" : [float_of_change, "name_of_change_function"]}
        """
        self.state_changes = state_changes
        """
        attributes contains a dictionary with all "secondary" attributes used
        for the computation of the utilities.
        """
        self.attributes = attributes
        """
        A list with dictionaries containing different states the action can
        be performed from.
        """
        self.possible_states = possible_states
    
    """
    The state change function returns the new value for the state. Its
    parameters are "state", which is the value of the current state, "change"
    which is the change-value and "fun", which is a string that implies which
    of the functions for calculating the new state is used.
    New functions can easily be added to this function.
    """
    def state_change_function(self, state, change, fun):
        # "Set" simply sets the new state to the value implied by the change.
        # The current state has no influence on the new state.
        if fun == "set":
            return change
        # "Add" adds the change to the current state(will mostly be used with
        # negative change-values to "subtract")
        if fun == "add":
            return state + change
        # "Mul" multiplies the current state by a change-factor.
        if fun == "mul":
            return state * change
        
"""
THe state-class is used o hold information for each state-item.
"""
class State:
    def __init__(self,
                 current = None,
                 desired = None,
                 threshold = 0.5):
        # The current state-value the agent is in
        self.current = current
        # THe desired state-value the agent would like to be in.
        self.desired = desired
        """
        The threshold defines the value from which on the agent feels like a
        change towards the desired state is needed, ultimately it is being used
        to convert the "current" state from a float-value to a boolean state
        that is either true or false.
        """
        self.threshold = threshold
        
""" Beginning of Example 1 """       

# King Orange's actions
orange_actions = {}
# Homefood
orange_actions["homefood"] = Action()
orange_actions["homefood"].state_changes = {"hungry" : [0, "set"]}
orange_actions["homefood"].attributes = {"quality":0.7,
                                         "low_price":0.9}
orange_actions["homefood"].possible_states = [{"hungry":True}]

# Febo
orange_actions["febo"] = Action()
orange_actions["febo"].state_changes = {"hungry" : [0, "set"]}
orange_actions["febo"].attributes = {"quality":0.2,
                                         "low_price":0.9}
orange_actions["febo"].possible_states = [{"hungry":True}]

# Michelin
orange_actions["michelin"] = Action()
orange_actions["michelin"].state_changes = {"hungry" : [0, "set"]}
orange_actions["michelin"].attributes = {"quality":0.8,
                                         "low_price":0.1}
orange_actions["michelin"].possible_states = [{"hungry":True}]

# King Orange's States
orange_states = {}
# Hungry
orange_states["hungry"] = State()
orange_states["hungry"].current = 1
orange_states["hungry"].desired = 0
orange_states["hungry"].threshold = 0.6


# Start of example Agent
king_orange = Agent(
        # values
        {"quality" : 0.9,
         "low_price" : 0.1,
         "hungry" : 0.8},
        # current state
        orange_states,
        # all actions
        orange_actions
        )      

# Tokkie's actions
tokkie_actions = {}
# Homefood
tokkie_actions["homefood"] = Action()
tokkie_actions["homefood"].state_changes = {"hungry" : [0, "set"]}
tokkie_actions["homefood"].attributes = {"quality":0.7,
                                         "low_price":0.9}
tokkie_actions["homefood"].possible_states = [{"hungry":True}]

# McBurgercrap
tokkie_actions["febo"] = Action()
tokkie_actions["febo"].state_changes = {"hungry" : [0, "set"]}
tokkie_actions["febo"].attributes = {"quality":0.2,
                                         "low_price":0.9}
tokkie_actions["febo"].possible_states = [{"hungry":True}]

# Michelin
tokkie_actions["michelin"] = Action()
tokkie_actions["michelin"].state_changes = {"hungry" : [0, "set"]}
tokkie_actions["michelin"].attributes = {"quality":0.8,
                                         "low_price":0.1}
tokkie_actions["michelin"].possible_states = [{"hungry":True}]

# King Orange's States
tokkie_states = {}
# Hungry
tokkie_states["hungry"] = State()
tokkie_states["hungry"].current = 1
tokkie_states["hungry"].desired = 0
tokkie_states["hungry"].threshold = 0.6

# Start of example Agent
tokkie = Agent(
        # values
        {"quality" : 0.3,
         "low_price" : 0.8,
         "hungry" : 0.8},
        # current state
        tokkie_states,
        # all actions
        tokkie_actions)
        


# Using act function of example Agent to see what 
print("\n---First example for comparison with the AATS-system---\n")
print("This example uses the same parameters than the AATS. It does not "
      "use the 'first stage' of evaluation, as there is only one state "
      "that is considered, 'hungry'.\n")
print("Computing king orange's actions: \n")
king_orange.act()
print("\n")
print("Computing tokkie's actions: \n")
tokkie.act()
print("\n")


""" Beginning of Example 2 """ 

# Tokkie's actions
tok_rel_actions = {}
# Homefood
tok_rel_actions["homefood"] = Action()
tok_rel_actions["homefood"].state_changes = {"hungry" : [0, "set"],
                                            "stressed" : [0.2, "add"]}
tok_rel_actions["homefood"].attributes = {"quality":0.7,
                                         "low_price":0.9}
tok_rel_actions["homefood"].possible_states = [{"hungry":True, "stressed":True},
                                              {"hungry":True, "stressed":False}]

# McBurgercrap
tok_rel_actions["febo"] = Action()
tok_rel_actions["febo"].state_changes = {"hungry" : [0, "set"],
                                                "stressed" : [-0.4, "add"]}
tok_rel_actions["febo"].attributes = {"quality":0.2,
                                         "low_price":0.9}
tok_rel_actions["febo"].possible_states = [{"hungry":True, "stressed":True},
                                                  {"hungry":True, "stressed":False}]

# Michelin
tok_rel_actions["michelin"] = Action()
tok_rel_actions["michelin"].state_changes = {"hungry" : [0, "set"],
                                            "stressed" : [-0.4, "add"]}
tok_rel_actions["michelin"].attributes = {"quality":0.8,
                                         "low_price":0.1}
tok_rel_actions["michelin"].possible_states = [{"hungry":True, "stressed":True},
                                              {"hungry":True, "stressed":False}]

# King Orange's States
tok_rel_states = {}
# Hungry
tok_rel_states["hungry"] = State()
tok_rel_states["hungry"].current = 1
tok_rel_states["hungry"].desired = 0
tok_rel_states["hungry"].threshold = 0.6

# Stressed
tok_rel_states["stressed"] = State()
tok_rel_states["stressed"].current = 0.4
tok_rel_states["stressed"].desired = 0
tok_rel_states["stressed"].threshold = 0.6


# Start of example Agent
tok_rel = Agent(
        # values
        {"quality" : 0.3,
         "low_price" : 0.8,
         "stressed" : 0.6,
         "hungry" : 0.8},
        # current state
        tok_rel_states,
        # all actions
        tok_rel_actions)


# Tokkie's actions
tok_str_actions = {}
# Homefood
tok_str_actions["homefood"] = Action()
tok_str_actions["homefood"].state_changes = {"hungry" : [0, "set"],
                                            "stressed" : [0.2, "add"]}
tok_str_actions["homefood"].attributes = {"quality":0.7,
                                         "low_price":0.9}
tok_str_actions["homefood"].possible_states = [{"hungry":True, "stressed":True},
                                              {"hungry":True, "stressed":False}]

# McBurgercrap
tok_str_actions["febo"] = Action()
tok_str_actions["febo"].state_changes = {"hungry" : [0, "set"],
                                                "stressed" : [-0.4, "add"]}
tok_str_actions["febo"].attributes = {"quality":0.2,
                                         "low_price":0.9}
tok_str_actions["febo"].possible_states = [{"hungry":True, "stressed":True},
                                                  {"hungry":True, "stressed":False}]

# Michelin
tok_str_actions["michelin"] = Action()
tok_str_actions["michelin"].state_changes = {"hungry" : [0, "set"],
                                            "stressed" : [-0.4, "add"]}
tok_str_actions["michelin"].attributes = {"quality":0.8,
                                         "low_price":0.1}
tok_str_actions["michelin"].possible_states = [{"hungry":True, "stressed":True},
                                              {"hungry":True, "stressed":False}]

# King Orange's States
tok_str_states = {}
# Hungry
tok_str_states["hungry"] = State()
tok_str_states["hungry"].current = 1
tok_str_states["hungry"].desired = 0
tok_str_states["hungry"].threshold = 0.6

# Stressed
tok_str_states["stressed"] = State()
tok_str_states["stressed"].current = 0.8
tok_str_states["stressed"].desired = 0
tok_str_states["stressed"].threshold = 0.6


# Start of example Agent
tok_str = Agent(
        # values
        {"quality" : 0.3,
         "low_price" : 0.8,
         "stressed" : 0.6,
         "hungry" : 0.8},
        # current state
        tok_str_states,
        # all actions
        tok_str_actions)
        
# Using act function of example Agent to see what happens
print("\n---Second example to present first level of comparison---\n")
print("This example adds a 'stressed'-state, representing the level of "
      "stress the agent is in. Building on the example-agent of 'Tokkie', "
      "the two examples that are used here are 'Tokkie relaxed', so "
      "Tokkie in a relaxed state, and 'Tokkie stressed', Tokkie in a stressed "
      "state. Both restaurants have a relaxing effect due to their atmosphere "
      "while homefood increases stress due to the effort needed to prepare "
      "food.\n")
print("Computing relaxed tokkie's actions:\n")
tok_rel.act()
print("\n")
print("Computing stressed tokkie's actions:\n")
tok_str.act()
print("\nAs with the previous example, the relaxed Tokkie has both "
      "restaurants as well as the homefood-actions available. The utilities "
      "and therefore the chosen action haven't changed. The stressed Tokkie "
      "however feels 'too stressed' to prepare food and therefore only "
      "considers going to the restaurant. The utilities are still the same, "
      "however limited to the restaurant, which is why the stressed Tokkie "
      "chooses to go to febo, ultimately relieving him from hunger and stress.")