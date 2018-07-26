from collections import UserList
class Synchrophasor(UserList):
    """
    time_tag is the time tag of the synchrophasor message
    arr_time is the unix time that the last data frame for the synchrophasor received 
    perf_counter is used the check the performace
    """
    def __init__(self, list_, time_tag, arr_time, perf_counter):
        super(Synchrophasor, self).__init__(list_)
        self.time = time_tag
        self.arr_time = arr_time
        self.perf_counter = perf_counter 