import copy
from pubsub import pub
import threading


class SingletonException(Exception):
    pass


class Singleton(object):
    __instance = None

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if cls.__instance == None:
            cls.__instance = cls(*args, **kwargs)
        return cls.__instance

    def __init__(self, *args, **kwargs):
        if self.__instance is not None:
            raise SingletonException("Class instance is already created")


class Store(Singleton):
    def __init__(self, reducers):
        super().__init__()

        self.__reducers = reducers
        self.__state = { r.__name__: r() for r in self.__reducers }

    def dispatch(self, action):
        if callable(action):
            thread = threading.Thread(
                target = action,
                args   = [self.dispatch, self.get_state]
            )
            thread.start()
        else:
            self.__state = {
                r.__name__: r(self.__state[r.__name__], action)
                for r in self.__reducers
            }

        self.update()

    def get_state(self):
        return copy.deepcopy(self.__state)

    def update(self):
        pub.sendMessage("update", state=self.get_state())

