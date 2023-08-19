# this file is currently unused
# need to satisfy LSP and only real way to is to make common FrameBatch input or something

# import abc

# from giford.frame.frame_batch import FrameBatch


# class AbstractAction(abc.ABC):
#     @abc.abstractmethod
#     def __init__(self, *args, **kwargs):
#         """
#         setup things for your action here

#         note: some things are better left as parameters for process
#         generally you'll want to create 1 action per image manipulation instance

#         i think by making this @abstract, it is no longer able to be skipped
#         this is preferable, so we are consistent with how things are called
#         """
#         pass

#     @abc.abstractmethod
#     def process(self, *args, **kwargs) -> FrameBatch:
#         """
#         take something and do something

#         Nothing->Something
#         Something->Something
#         Something->Nothing
#         """
#         pass
