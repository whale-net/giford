from giford.frame_batch import FrameBatch
from .abstract_action import AbstractAction

# done - do i need both *args and **kwargs?
# i think yes, *args for positional, **kwargs for keyword
# if not both, may get weird warnings depending on usage


class AbstractFrameAction(AbstractAction):
    """
    really no reason for this class
    just kind of feels like a good idea for better inheritance tree shape
    """

    def __init__(self):
        pass

    def process(self, *args, **kwargs) -> FrameBatch:
        """
        takes in frame(s), produces frame(s)
        """
        pass


class ChainFrameAction(AbstractFrameAction):
    def __init__(self):
        super().__init__()

    def process(self, input_batch: FrameBatch, *args, **kwargs) -> FrameBatch:
        """
        takes in frame(s), produces frame(s)
        """
        pass
