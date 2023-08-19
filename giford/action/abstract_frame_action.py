import abc

from giford.frame.frame_batch import FrameBatch

# from .abstract_action import AbstractAction

# done - do i need both *args and **kwargs?
# i think yes, *args for positional, **kwargs for keyword
# if not both, may get weird warnings depending on usage


# TODO - inherit from AbstractAction
# will need to define base class for FrameBatch inputs
# in order to not violate LSP
class AbstractFrameAction:
    """
    take in input_batch, produce output_batch
    """

    @abc.abstractmethod
    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def process(self, input_batch: FrameBatch) -> FrameBatch:
        """
        takes in frame(s), produces frame(s)
        """
        pass
