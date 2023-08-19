# i think `from giford import action` is ugly
# the submodule names are common and are confusing if imported directly
# preferred usages are:
# `from giford.action import Swirl`
# `import giford` and `giford.action.Swirl`
# if you must have `action`, do `import giford.action as action` instead
# otherwise, if there is a legit reason to have these exposed here then let me know

# from . import action as action
# from . import frame as frame
# from . import image as image
# from . import util as util
