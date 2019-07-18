import statistics
import timeit
import re


class timer(object):

    dict_duration = {}
    path_block_current = ""
    flg_suspend = False

    def __init__(self,
                name,
                n_digit=3,
                flg_share_path_block=True):
        """record execution time for code block
           
            args
                name
                    str
                    code block name for identifying the record.
                    duration is recorded as a dict of list.
                    the key is block name, which is sequentially added to outer block name.
                    duration is recorded on exit.
                n_digit
                    int
                    rounding point for the duration.
                flg_share_path_block
                    bool
                    whether or not use shared block path as entry name between instances
                    its useful to track time in nested structure.
                    take care when use both shared block path and multi threading.
                    it may fail to track nested structure.
        """

        self.name_block = name
        self.n_digit = n_digit
        self.flg_share_path_block = flg_share_path_block

    def enter_block(self):
        """initialize for recording code block

        """

        # set start time
        self.time_start = timeit.default_timer()
        self.time_prev = timeit.default_timer()
        # add block name to shared current block path
        self.path_block_outer = timer.path_block_current
        if self.flg_share_path_block:
            timer.path_block_current = "/".join(
                [timer.path_block_current, self.name_block]
            ) 

    def __enter__(self):
        self.enter_block()
        return self

    def _record_time(self,
                    name_entry=[],
                    time_prev=timeit.default_timer() ):
        if timer.flg_suspend:
            return
        # use shared path
        if self.flg_share_path_block:
            path_entry = "/".join(
                    [timer.path_block_current] + name_entry
            )
        else:
            path_entry = "/".join(
                    [self.name_block] + name_entry
            )
        duration = timeit.default_timer() - time_prev
        timer.dict_duration.setdefault(path_entry, []).append(
            round(duration, self.n_digit)
        )

    def record_time(self, name_entry):
        """record elapsed time within the block
            args
                name_entry
                    str
                    entry name for identifying the record.
                    duration is recorded as dict of list.
                    the key is current block path + entry name.
                    duration is calculated from the previouse recorded point.
                    otherwise, beginning of the block.
        """
        self._record_time(name_entry=[name_entry], time_prev=self.time_prev)
        self.time_prev = timeit.default_timer()

    def exit_block(self):
        """finalize for recording code block

        """

        self._record_time(time_prev=self.time_start)
        # reset current block path
        timer.path_block_current = self.path_block_outer

    def __exit__(self, type, value, traceback):
        self.exit_block()

    @staticmethod
    def get_stats(n_digit=3, filter="", dict_func_stats=None):
        """summarize recorded entries
            args
                n_digit
                    int
                    rounding point for the statistics.
                filter
                    str
                    filter entries.
                    you can use regular expressions.
                dict_func_stats
                    dict
                    summarize entries using arbitrary functions in addition to sum and mean.
        """
        _re = re.compile(filter)
        dict_mean = {
            k : round(statistics.mean(v), n_digit)
            for k, v in timer.dict_duration.items()
            if _re.search(k)
        }
        dict_sum = {
            k : round(sum(v), n_digit)
            for k, v in timer.dict_duration.items()
            if _re.search(k)
        }
        dict_stats = {"mean":dict_mean, "sum":dict_sum}
        if dict_func_stats is not None:
            for name, func in dict_func_stats.items():
                dict_any_stats = {
                    k : round(func(v), n_digit)
                    for k, v in timer.dict_duration.items()
                    if _re.search(k)
                }
                dict_stats[name] = dict_any_stats
        return dict_stats


def capture(name=None,
            n_digit=3,
            flg_share_path_block=True,
            name_obj_timer=None
):
    """record execution time for functions, 
        please use as a decorator
           
            args
                name
                    str
                    code block name for identifying the record.
                    duration is recorded as a dict of list.
                    the key is block name, which is sequentially added to outer block name.
                    duration is recorded on exit.
                n_digit
                    int
                    rounding point for the duration.
                flg_share_path_block
                    bool
                    whether or not use shared block path as entry name between instances
                    its useful to track time in nested structure.
                    take care when use both shared block path and multi threading.
                    it may fail to track nested structure.
                name_obj_timer
                    str
                    symbol name for referencing nestimer.timer instance inside the function.
    """

    def _capture(function, *args, **kwargs):

        def _func(*args, **kwargs):

            # set block name
            name_func = function.__name__
            if name is None:
                name_block = name_func
            else:
                name_block = name

            
            # start recording
            with timer(name=name_block, n_digit=n_digit, flg_share_path_block=flg_share_path_block) as t :
                # execute functions
                if name_obj_timer is None:
                    result = function(*args, **kwargs)
                else:
                    _dict = {name_obj_timer : t}
                    kwargs.setdefault(name_obj_timer, None)
                    kwargs.pop(name_obj_timer)
                    result = function(*args, **kwargs, **_dict)
                    
                return result

        return _func

    return _capture
