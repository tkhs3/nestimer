measuring/recording code execution time in nested structure



# How/What is this #
- measure/record execution time in detail and easily



# Why/Objective #
1. to help reduce/optimize code execution time
2. by visualizing where bottleneck is
3. by measuring execution time of code blocks in nested strucre



# Value/What is different #
- tracking in nested structure
- lifelong tracking
- minimum code injections




# Example #

    # define modules 
    import nestimer
    import time

    @nestimer.capture()
    def _loop(n_loop=3, n_sleep=1):
        for i in range(n_loop):
        time.sleep(n_sleep)
    
    @nestimer.capture()
    def nest2():
        _loop(n_loop=2,n_sleep=2)
    
    @nestimer.capture()
    def nest1():
        _loop(n_loop=1,n_sleep=1)
        time.sleep(1)
        nest2()
    
    @nestimer.capture()
    def main():
        time.sleep(1)
        nest1()

    # run modules
    main()
    main()
    main()

    #　show the result
    nestimer.timer.get_stats()

    > {'mean': {'/main/nest1/_loop': 1.015,
    >   '/main/nest1/nest2/_loop': 4.03,
    >   '/main/nest1/nest2': 4.03,
    >   '/main/nest1': 6.061,
    >   '/main': 7.075},
    >  'sum': {'/main/nest1/_loop': 3.046,
    >   '/main/nest1/nest2/_loop': 12.09,
    >   '/main/nest1/nest2': 12.09,
    >   '/main/nest1': 18.183,
    >   '/main': 21.226}}



# Use case scenario #

    # define modules
    import nestimer
    import time
    
    @nestimer.capture()
    def init():
        time.sleep(1)
    
    @nestimer.capture()
    def load_data():
        time.sleep(1)
    
    @nestimer.capture()
    def build_model():
        time.sleep(1)
    
    @nestimer.capture()
    def get_batch():
        time.sleep(0.1)
    
    @nestimer.capture()
    def train_on_batch():
        time.sleep(0.1)
    
    @nestimer.capture()
    def train_model():
        for i_epoch in range(10):
            for i_step in range(10): 
                get_batch()
                train_on_batch()
    
    @nestimer.capture()
    def main():
        init()
        load_data()
        build_model()
        train_model()

    # run a module
    main()

    # show the result
    nestimer.timer.get_stats()

    > {'mean': {'/main/init': 1.001,
    >   '/main/load_data': 1.015,
    >   '/main/build_model': 1.016,
    >   '/main/train_model/get_batch': 0.109,
    >   '/main/train_model/train_on_batch': 0.109,
    >   '/main/train_model': 21.869,
    >   '/main': 24.902},
    >  'sum': {'/main/init': 1.001,
    >   '/main/load_data': 1.015,
    >   '/main/build_model': 1.016,
    >   '/main/train_model/get_batch': 10.909,
    >   '/main/train_model/train_on_batch': 10.908,
    >   '/main/train_model': 21.869,
    >   '/main': 24.902}}




# How to install #

    pip install nestimer




# How to use #
    
##  how to measure ##

1. measure functions

        @nestimer.caputure
        def any_functions()
            pass

2. measure a whole code block and elapsed time within the code block

        import nestimer
        import time
    
        with nestimer.timer(name="this name is recorded as entry") as timer:
            time.sleep(1)
            timer.record_time("done something 1")
            time.sleep(2)
            timer.record_time("done something 2")
    
        nestimer.timer.get_stats()

        > {'mean': {'/this name is recorded as entry/done something 1': 1.001,
        >   '/this name is recorded as entry/done something 2': 2.015,
        >   '/this name is recorded as entry': 3.016},
        >  'sum': {'/this name is recorded as entry/done something 1': 1.001,
        >   '/this name is recorded as entry/done something 2': 2.015,
        >   '/this name is recorded as entry': 3.016}}

3. measure a whole code block and elapsed time without with statement
 
        import nestimer
        import time
    
        timer = nestimer.timer(name="this name is recorded as entry")
        timer.enter_block()
        time.sleep(1)
        timer.record_time("done something 1")
        time.sleep(2)
        timer.record_time("done something 2")
        timer.exit_block()

        nestimer.timer.get_stats()

        > {'mean': {'/this name is recorded as entry/done something 1': 1.015,
        >   '/this name is recorded as entry/done something 2': 2.015,
        >   '/this name is recorded as entry': 3.031},
        >  'sum': {'/this name is recorded as entry/done something 1': 1.015,
        >   '/this name is recorded as entry/done something 2': 2.015,
        >   '/this name is recorded as entry': 3.031}}

## how to check ##

1. check simple statistics

        nestimer.timer.get_stats()

        > {'mean': {'/main/init': 1.001,
        >   '/main/load_data': 1.015,
        >   '/main/build_model': 1.016,
        >   '/main/train_model/get_batch': 0.109,
        >   '/main/train_model/train_on_batch': 0.109,
        >   '/main/train_model': 21.869,
        >   '/main': 24.902},
        >  'sum': {'/main/init': 1.001,
        >   '/main/load_data': 1.015,
        >   '/main/build_model': 1.016,
        >   '/main/train_model/get_batch': 10.909,
        >   '/main/train_model/train_on_batch': 10.908,
        >   '/main/train_model': 21.869,
        >   '/main': 24.902}}

2. check any statistics you want
    
        nestimer.timer.get_stats(
            dict_func_stats={"median":statistics.median}
        )
        
        > {'mean': {'/main/init': 1.001,
        >   '/main/load_data': 1.015,
        >   '/main/build_model': 1.016,
        >   '/main/train_model/get_batch': 0.109,
        >   '/main/train_model/train_on_batch': 0.109,
        >   '/main/train_model': 21.869,
        >   '/main': 24.902},
        >  'sum': {'/main/init': 1.001,
        >   '/main/load_data': 1.015,
        >   '/main/build_model': 1.016,
        >   '/main/train_model/get_batch': 10.909,
        >   '/main/train_model/train_on_batch': 10.908,
        >   '/main/train_model': 21.869,
        >   '/main': 24.902},
        >  'median': {'/main/init': 1.001,
        >   '/main/load_data': 1.015,
        >   '/main/build_model': 1.016,
        >   '/main/train_model/get_batch': 0.109,
        >   '/main/train_model/train_on_batch': 0.109,
        >   '/main/train_model': 21.869,
        >   '/main': 24.902}}
    


3. check the statistics for filtered entries

        nestimer.timer.get_stats(
            filter="train"
        )

        > {'mean': {'/main/train_model/get_batch': 0.109,
        >   '/main/train_model/train_on_batch': 0.109,
        >   '/main/train_model': 21.869},
        >  'sum': {'/main/train_model/get_batch': 10.909,
        >   '/main/train_model/train_on_batch': 10.908,
        >   '/main/train_model': 21.869}}