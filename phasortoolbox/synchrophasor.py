from collections import UserList


def _kaitai_show(self, parent_path='    '):
    if type(self) in (int, float, str, bytes, bool):
        print(" == ".join((parent_path, self.__repr__())))
    elif type(self) == list:
        for i, item in enumerate(self):
            try:
                item.show('{}[{}]'.format(parent_path,i))
            except:
                _kaitai_show(item,'{}[{}]'.format(parent_path,i))
    else:
        for item in sorted(vars(self)):
            if not item.startswith('_'):
                _r = getattr(self, item)
                try:
                    _r.show(parent_path+'.'+item)
                except:
                    _kaitai_show(_r,parent_path+'.'+item)


class Synchrophasor(UserList):
    """
    time_tag is the time tag of the synchrophasor message
    arr_time is the unix time that the last data frame for the synchrophasor received 
    perf_counter is used the check the performace
    """

    def __repr__(self):
        _repr_list = []
        for item in vars(self):
            if not item.startswith('_'):
                _r = getattr(self, item)
                if type(_r) in (int, float, str, bytes):
                    _repr_list.append("=".join((item, _r.__repr__())))
                else:
                    _repr_list.append(item)
        return "<" + self.__class__.__name__ + " |" + ", ".join(_repr_list) + ">"


    def __init__(self, list_, time_tag, arr_time, perf_counter):
        super(Synchrophasor, self).__init__(list_)
        self.time = time_tag
        self.arr_time = arr_time
        self.perf_counter = perf_counter 


    def show(self, parent_path='    '):
        _kaitai_show(self, parent_path)