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




king_orange = Agent(
        # values
        {"quality" : 0.9,
         "low_price" : 0.05,
         "low_effort" : 0.5},
        # current state
        {"hungry":True},
        # all states
            ### What is the difference here between states and actions?
        [{"hungry":True},
         {"hungry":False}],
        # all actions
            ### the values are their possibilities right?
        {"homefood":
             {"quality":0.1,
              "low_price":0.95,
              "low_effort":0.9},
         "mcburgercrap":
             {"quality":0.2,
              "low_price":0.85,
              "low_effort":0.7},
         "michelin":
             {"quality":0.8,
              "low_price":0.1,
              "low_effort":0.7}},
        # all possible actions
            ### isn't it more convenient to write it down like this: ?
            ### {"hungry":
            ###     ["homefood",
            ###     "mcburgercrap",
            ###     "michelin"]}
        {"homefood" : "hungry",
         "mcburgercrap" : "hungry",
         "michelin" : "hungry"}
        )


class State:
    def __init__(self):
        pass
