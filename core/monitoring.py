from abc import ABCMeta, abstractmethod
from threading import Timer


class AbcMonitor(metaclass=ABCMeta):
    """Base class for entities, which require repeating event.

    Attributes:
        monitoring (bool): indicator activity of monitor.
        monitoring_latency (int, float): frequency of execution monitor's action.
    """

    # region initialization

    def __init__(self, monitoring_latency):
        self.__monitoring_latency = None
        self.monitoring_latency = monitoring_latency
        self.__monitoring = False

    # endregion

    # region properties

    @property
    def monitoring(self):
        return self.__monitoring

    @property
    def monitoring_latency(self):
        return self.__monitoring_latency

    @monitoring_latency.setter
    def monitoring_latency(self, value):
        self.__monitoring_latency = value

    # endregion

    # region methods & abstract methods

    def start_monitoring(self):
        """Enable periodically monitoring.
        """
        if self.__monitoring is False:
            self.__monitoring = True
            self.__monitoring_action()

    def stop_monitoring(self):
        """Disable periodically monitoring.
        """
        self.__monitoring = False

    def __monitoring_action(self):
        if self.__monitoring is True:
            self._monitoring_action()
            Timer(self.monitoring_latency, self.__monitoring_action).start()

    @abstractmethod
    def _monitoring_action(self):
        """Action, which repeated, when monitoring is enabled.
        """
        raise NotImplementedError('Method not implemented by derived class!')

    # endregion

    pass