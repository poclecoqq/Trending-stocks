class ProgressBar:
    def __init__(self, total=0):
        self.total = total
        self.iteration = 0
    
    def step_done(self):
        self.iteration += 1
        self.printProgressBar()

    # code taken from https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    def printProgressBar (self, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (self.iteration / float(self.total)))
        filledLength = int(length * self.iteration // self.total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
        # Print New Line on Complete
        if self.iteration == self.total: 
            print()