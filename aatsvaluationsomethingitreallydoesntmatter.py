# -*- coding: utf-8 -*-

class Agent:
    # initializing the agent. The last 4 attributes are empty if not provided
    # and can be added afterwards as well
    def __init__(self,
                 values,
                 curr_state,
                 all_states={},
                 all_actions={},
                 poss_actions={},
                 sys_transition={}):  ### What is sys_transition?
        # values is a dictionary containing the personal values of the agent.
        self.values = values
        # curr_state is the state an agent is in at the moment
        self.curr_state = curr_state
        # all_states are all possible states an agent could be in
        self.all_states = all_states
        # all_actions are all possible actions an agent could take
        self.all_actions = all_actions
        # poss_actions is a dictionary containing an entry for each action
        # which lists all states that this action can be taken from.
        self.poss_actions = poss_actions


    # Adding a new dictionary of values to the existing values.
    # Careful: Existing values will be overwritten!
    def update_values(self, new_values):
        self.values.update(new_values)

    # Making the agent act based on its current state
    def act(self):
        # For loops through list of possible action-state pairings to
        # see which ones are possible from current state
        def curr_act():
            curr_actions = []
            for i in self.poss_actions:
                for j in self.poss_actions[i]:
                    if j == self.curr_state:
                        curr_actions.append(i)
            return curr_actions
        
        # Valuation Function to calculate utilities of all poss. actions
        def val_function(curr_actions):
            utility_list = []
            for i in curr_actions:
                utility = 0
                curr_act_dict = self.all_actions[i]
                curr_act_dict = curr_act_dict[1]
                for j in curr_act_dict:
                    utility += curr_act_dict[j] * self.values[j]
                utility_list.append([utility, i])
            return sorted(utility_list, reverse=True)
        
        # Getting all possible actions at this moment
        print("Current State: " + str(self.curr_state))
        curr_actions = curr_act()
        print("Possible Actions: " + str(curr_actions))
        
        # Calculating valuation
        curr_utilities = val_function(curr_actions)
        print("Utilities of actions: ")
        for i in curr_utilities:
            print(str(i[1]) + ": " + str(i[0]))
        
        # Showing best action
        chosen_action = curr_utilities[0]
        print("Chosen action by agent: " + chosen_action[1])
        
        # Updating current state
        ca_statchange = self.all_actions[chosen_action[1]][0]
        for i in ca_statchange:
            self.curr_state[i] = ca_statchange[i]
        print("New State: " + str(self.curr_state))

        

king_orange = Agent(
        # values
        {"hungry" : 1.,
         "quality" : 0.9,
         "low_price" : 0.05,
         "low_effort" : 0.5},
        # current state
        {"hungry" : True},
        # all states
            ### What is the difference here between states and actions?
            # The state of being hungry is basically here to provide a state
            # from which the action(eating at the restaurant) can be taken.
            # The reason I used this was simply because I follow the paper
        [{"hungry":True},
         {"hungry":False}],
        # all actions
            ### the values are their possibilities right?
            # Yes, although there are different theoretical interpretations
            # regarding their meaning. You can say "probability of outcome"
            # you can also just say "average subjective positive gain",
            # whatever the positive then means to the person.
        {"homefood":
             [{"hungry":False},
              {"quality":0.1,
               "low_price":0.95,
               "low_effort":0.9}],
         "mcburgercrap":
             [{"hungry":False},
              {"quality":0.2,
              "low_price":0.85,
              "low_effort":0.7}],
         "michelin":
             [{"hungry":False},
              {"quality":0.8,
              "low_price":0.1,
              "low_effort":0.7}]},
        # all possible actions
            ### isn't it more convenient to write it down like this: ?
            ### {"hungry":
            ###     ["homefood",
            ###     "mcburgercrap",
            ###     "michelin"]}
            # I'm strictly following the way it is in the paper right now
            # The reasoning here is that for every action there are all
            # statuses listed that can be taken, which makes it easier to
            # access this list, however, one could also simply use a loop for
            # that. Especially in simple cases like these your way of writing
            # would obviously be much more convenient.
        {"homefood" : [{"hungry":True}],
         "mcburgercrap" : [{"hungry":True}],
         "michelin" : [{"hungry":True}]}
        )


class State:
    def __init__(self):
        pass

king_orange.act()
