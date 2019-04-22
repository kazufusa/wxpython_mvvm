from datetime import datetime
from pubsub import pub
import time
import threading


class Action():
    def __init__(self, mytype, payload=None):
        self.__type = mytype
        self.__payload = payload

    @property
    def type(self):
        return self.__type

    @property
    def payload(self):
        return self.__payload


def start_job(*args):
    def job(dispatch, get_state):
        ident = threading.get_ident()
        dispatch(Action('START_JOB', dict(ident=ident)))

        dispatch(add_log("# start\n"))
        for i in range(5):
            time.sleep(1)

            state = get_state()
            if not state['job']['job_ident'] == ident: return
            dispatch(add_log(f"{datetime.now()}\n"))

        dispatch(add_log("# end\n"))

        dispatch(finish_job())

    return job

def finish_job():
    return Action('FINISH_JOB')

def add_log(text):
    return Action('ADD_LOG', dict(text=text))
