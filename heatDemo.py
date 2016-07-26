from clientInterface import clientInterface
from controller import controller

class heatDemo:
    def __init__(self):
        self.controller = controller()
        self.ci = clientInterface(self.controller)

    def run(self):
        self.ci.runApp()

if __name__ == '__main__':
    heat = heatDemo()
    heat.run()
