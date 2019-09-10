from LogImplementer import LogImplementer
import logging
class Foo(LogImplementer):

    def __init__(self):
        LogImplementer.__init__(self)


    def hello(self):
        self.logger.info('Hello world')
        self.logger.debug('This is a debug message')
        self.logger.warn('This is a warning')
        self.logger.error('Something has gone wrong')
        self.logger.critical('ERROR, CRITICAL FAILURE, ISAAC IS SELF-AWARE!')

foo = Foo()
foo.hello()


class Bar(Foo):
    def __init__(self):
        Foo.__init__(self)

    def subclassHello(self):
        self.logger.info('Hello from the subclass')

        self.logger.debug('Bye from the subclass')

bar = Bar()
bar.subclassHello()
