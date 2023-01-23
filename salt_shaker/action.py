import abc
from typing import Any, Union

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
    def process(self, *args, **kwargs) -> Union[Any, None]:
        """
        take something and do something

        Nothing->Something
        Something->Something
        Something->Nothing
        """
        pass
