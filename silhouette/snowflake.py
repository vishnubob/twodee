
class Environment(object):
    def __init__(self):
        pass
        

class Cursor(object):
    def __init__(self, environment):
        self.rules = []
        self.position = (0, 0)
        self.vector = (1, 0)
        self.steps = 0

    def step(self):
        # do we stop?
        if self.steps > self.max_steps:
            return 0
        self.steps += 1
        # 
        self.environment.write(
        
