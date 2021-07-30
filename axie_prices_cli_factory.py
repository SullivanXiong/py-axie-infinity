from abc import ABC

class Mode(ABC):
    @

def factory(mode):
    if mode == 'l' or mode == 'list':
        ListMode()
    elif mode == 'a' or mode == 'add':
        AddMode()