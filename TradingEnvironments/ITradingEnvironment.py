import abc

class ITradingEnvironment(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook_(cls, subclass):
        return (hasattr(subclass, 'get_price') and
                callable(subclass.get_price))
