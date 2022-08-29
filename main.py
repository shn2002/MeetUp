# Main file to call the controller

from mvc import *

controller = Controller(View(), Model())
controller.run()