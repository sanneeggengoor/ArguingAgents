# -*- coding: utf-8 -*-
"""

"""
class Agent:
    # initializing the agent. The last 2 attributes are empty if not provided
    # and can be added afterwards as well
    def __init__(self,
                 values,
                 curr_state,
                 desired_state={},
                 all_actions={}):
        # values is a dictionary containing the personal values of the agent.
        self.values = values
        # curr_state is the state an agent is in at the moment. It is a
        # dictionary consisting of attribute-value pairings, so far booleans.
        self.curr_state = curr_state
        # State that at this moment is desired
        self.desired_state = desired_state
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
        # For loops through list of possible action-state pairings to
        # see which ones are actable based on current state, returns list.
        def curr_poss_act():
            curr_actions = []
            for i in self.all_actions:
                for j in self.all_actions[i].possible_states:
                    if j == self.curr_state:
                        curr_actions.append(i)
            return curr_actions
        
        def curr_des_act(actions):
            curr_actions = {}
            for i in actions:
                target_meter = 0
                for j in self.desired_state:
                    if j in self.all_actions[i].state_changes:
                        if self.desired_state[j] == self.all_actions[i].state_changes[j]:
                            target_meter += 1
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
        print("Current State: " + str(self.curr_state))
        curr_actions = curr_poss_act()
        print("Possible Actions: " + str(curr_actions))
        
        # Calculating desired state actions
        curr_actions = curr_des_act(curr_actions)
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
            self.curr_state[i] = ca_statchange[i]
        print("New State: " + str(self.curr_state))

class Action:
    def __init__(self,
                 state_changes = {}, 
                 attributes = {}, 
                 possible_states = []):
        self.state_changes = state_changes
        self.attributes = attributes
        self.possible_states = possible_states
        
        
# King Orange's actions
orange_actions = {}
# Homefood
orange_actions["homefood"] = Action()
orange_actions["homefood"].state_changes = {"hungry" : False}
orange_actions["homefood"].attributes = {"quality":0.1,
                                         "low_price":0.95,
                                         "low_effort":0.9}
orange_actions["homefood"].possible_states = [{"hungry":True}]

# McBurgercrap
orange_actions["mcburgercrap"] = Action()
orange_actions["mcburgercrap"].state_changes = {"hungry" : False}
orange_actions["mcburgercrap"].attributes = {"quality":0.2,
                                         "low_price":0.85,
                                         "low_effort":0.7}
orange_actions["mcburgercrap"].possible_states = [{"hungry":True}]

# Michelin
orange_actions["michelin"] = Action()
orange_actions["michelin"].state_changes = {"hungry" : False}
orange_actions["michelin"].attributes = {"quality":0.8,
                                         "low_price":0.1,
                                         "low_effort":0.7}
orange_actions["michelin"].possible_states = [{"hungry":True}]

    

# Start of example Agent
king_orange = Agent(
        # values
        {"quality" : 0.9,
         "low_price" : 0.05,
         "low_effort" : 0.5},
        # current state
        {"hungry" : True},
        # desired state
        {"hungry" : False},
        # all actions
        orange_actions
        )

# Empty class for State, so far placeholder
class State:
    def __init__(self):
        pass

# Using act function of example Agent to see what happens
king_orange.act()
