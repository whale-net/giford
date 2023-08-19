import abc

from giford.frame.frame_batch import FrameBatch
from .abstract_action import AbstractAction

# done - do i need both *args and **kwargs?
# i think yes, *args for positional, **kwargs for keyword
# if not both, may get weird warnings depending on usage


class AbstractFrameAction(AbstractAction):
    """
    really no reason for this class
    just kind of feels like a good idea for better inheritance tree shape
    """

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def process(self, *args, **kwargs) -> FrameBatch:
        """
        takes in frame(s), produces frame(s)
        """
        pass


class ChainFrameAction(AbstractFrameAction):
    @abc.abstractmethod
    def __init__(self):
        super().__init__()

    @abc.abstractmethod
    def process(self, input_batch: FrameBatch, *args, **kwargs) -> FrameBatch:
        """
        takes in frame(s), produces frame(s)
        """
        pass
