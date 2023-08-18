import abc

from giford.frame_batch import FrameBatch


# done - do i need both *args and **kwargs?
# i think yes, *args for positional, **kwargs for keyword
# if not both, may get weird warnings depending on usage


class Action(abc.ABC):
    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        """
        setup things for your action here

        note: some things are better left as parameters for process
        generally you'll want to create 1 action per image manipulation instance

        i think by making this @abstract, it is no longer able to be skipped
        this is preferable, so we are consistent with how things are called
        """
        pass

    @abc.abstractmethod
    def process(self, *args, **kwargs) -> FrameBatch:
        """
        take something and do something

        Nothing->Something
        Something->Something
        Something->Nothing
        """
        pass


class ImageAction(Action):
    """
    really no reason for this class
    just kind of feels like a good idea for better inheritance tree shape
    """

    def __init__(self):
        pass

    def process(self, *args, **kwargs) -> FrameBatch:
        """
        takes in image(s), produces image(s)
        """
        pass


class ChainImageAction(ImageAction):
    def __init__(self):
        super().__init__()

    def process(self, input_batch: FrameBatch, *args, **kwargs) -> FrameBatch:
        """
        takes in image(s), produces image(s)
        """
        pass
