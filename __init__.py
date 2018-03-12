from core import *
import gui

def reload_all_modules():
    import core
    import gui
    reload(core)
    reload(gui)
