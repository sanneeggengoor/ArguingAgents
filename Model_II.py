# -*- coding: utf-8 -*-
"""

"""
class Agent:
    # initializing the agent. The last 2 attributes are empty if not provided
    # and can be added afterwards as well
    def __init__(self,
                 values,
                 states,
                 all_actions={}):
        # values is a dictionary containing the personal values of the agent.
        self.values = values
        # curr_state is the state an agent is in at the moment. It is a
        # dictionary consisting of attribute-value pairings, so far booleans.
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
        def curr_state():
            current_state_dict = {}
            current_state_prints = []
            desired_state = {}
            for i in self.states:
                state = self.states[i]
                if state.current >= state.threshold:
                    current_state_dict[i] = True
                    current_state_prints.append([i, state.current])
                    desired_state[i] = state.desired
                else:
                    current_state_dict[i] = False
            return current_state_dict, current_state_prints, desired_state
                    
        # For loops through list of possible action-state pairings to
        # see which ones are actable based on current state, returns list.
        def curr_poss_act(current_state_dict):
            curr_actions = []
            for i in self.all_actions:
                for j in self.all_actions[i].possible_states:
                    if j == current_state_dict:
                        curr_actions.append(i)
            return curr_actions
        
        def curr_des_act(actions, desired_state):
            curr_actions = {}
            for i in actions:
                target_meter = 0
                for j in desired_state:
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

        # Valuation Function to calculate utilities of all poss. actions
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

        # Getting all possible actions at this moment
        current_state_dict, current_state_prints, desired_state = curr_state()
        print("Current State: " + str(current_state_prints))
        curr_actions = curr_poss_act(current_state_dict)
        print("Possible Actions: " + str(curr_actions))
        
        # Calculating desired state actions
        curr_actions = curr_des_act(curr_actions, desired_state)
        print("Actions with most desired states: " + str(curr_actions))

        # Calculating valuation
        curr_utilities = val_function(curr_actions)
        print("Utilities of actions: ")
        for i in curr_utilities:
            print(str(i[1]) + ": " + str(i[0]))

        # Showing best action
        chosen_action = curr_utilities[0]
        print("Chosen action by agent: " + chosen_action[1])

        # Updating current state
        ca_statchange = self.all_actions[chosen_action[1]].state_changes
        for i in ca_statchange:
            changes = ca_statchange[i]
            self.states[i].current = self.all_actions[chosen_action[1]].state_change_function(self.states[i].current,
                       changes[0], changes[1])
        current_state_dict, current_state_prints, desired_state = curr_state()
        print("New State: " + str(current_state_prints))

class Action:
    def __init__(self,
                 state_changes = {},
                 attributes = {}, 
                 possible_states = []):
        self.state_changes = state_changes
        self.attributes = attributes
        self.possible_states = possible_states
    def state_change_function(self, state, change, fun):
        if fun == "set":
            return change
        if fun == "add":
            return state + change
        if fun == "mul":
            return state * change
        
# Empty class for State, so far placeholder
class State:
    def __init__(self,
                 current = None,
                 desired = None,
                 threshold = 0.5):
        self.current = current
        self.desired = desired
        self.threshold = threshold
        
        
# King Orange's actions
orange_actions = {}
# Homefood
orange_actions["homefood"] = Action()
orange_actions["homefood"].state_changes = {"hungry" : [0, "set"]}
orange_actions["homefood"].attributes = {"quality":0.1,
                                         "low_price":0.95,
                                         "low_effort":0.9}
orange_actions["homefood"].possible_states = [{"hungry":True}]

# McBurgercrap
orange_actions["mcburgercrap"] = Action()
orange_actions["mcburgercrap"].state_changes = {"hungry" : [0, "set"]}
orange_actions["mcburgercrap"].attributes = {"quality":0.2,
                                         "low_price":0.85,
                                         "low_effort":0.7}
orange_actions["mcburgercrap"].possible_states = [{"hungry":True}]

# Michelin
orange_actions["michelin"] = Action()
orange_actions["michelin"].state_changes = {"hungry" : [0, "set"]}
orange_actions["michelin"].attributes = {"quality":0.8,
                                         "low_price":0.1,
                                         "low_effort":0.7}
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
         "low_price" : 0.05,
         "low_effort" : 0.5,
         "hungry" : 0.8},
        # current state
        orange_states,
        # all actions
        orange_actions
        )


        

# Using act function of example Agent to see what happens
king_orange.act()
