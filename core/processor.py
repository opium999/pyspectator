import psutil
import platform
import os
import subprocess
import re
from .monitoring import AbcMonitor
from collections import Callable


class Processor(AbcMonitor):

    def __init__(self, monitoring_latency):
        super().__init__(monitoring_latency)
        self.__count = psutil.cpu_count()
        self.__percent = psutil.cpu_percent()
        self.__name = Processor.__get_processor_name()
        self.__temperature = None
        self.__temperature_reader = Processor.__get_processor_temperature_reader()

    @property
    def name(self):
        return self.__name

    @property
    def count(self):
        return self.__count

    @property
    def percent(self):
        return self.__percent

    @property
    def temperature(self):
        return self.__temperature

    def _monitoring_action(self):
        self.__percent = psutil.cpu_percent()
        if isinstance(self.__temperature_reader, Callable):
            self.__temperature = self.__temperature_reader()

    @classmethod
    def __get_processor_name(cls):
        cpu_name = None
        os_name = platform.system()
        if os_name == 'Windows':
            cpu_name = platform.processor()
        elif os_name == 'Darwin':
            os.environ['PATH'] = os.environ['PATH'] + os.pathsep + '/usr/sbin'
            command = 'sysctl -n machdep.cpu.brand_string'
            cpu_name = subprocess.check_output(command).strip()
        elif os_name == 'Linux':
            all_info = subprocess.check_output('cat /proc/cpuinfo', shell=True).strip()
            for line in all_info.split(os.linesep.encode()):
                line = line.decode()
                if 'model name' in line:
                    cpu_name = re.sub('.*model name.*:', str(), line, 1).strip()
                    break
        return cpu_name

    @classmethod
    def __get_processor_temperature_reader(cls):
        func = None
        os_name = platform.system()
        if os_name == 'Windows':
            import wmi
            func = lambda: wmi.WMI(namespace='root\\wmi').MSAcpi_ThermalZoneTemperature()[0].CurrentTemperature / 10.0 - 273.15
        elif os_name == 'Darwin':
            pass
        elif os_name == 'Linux':
            if os.path.exists('/sys/devices/LNXSYSTM:00/LNXTHERM:00/LNXTHERM:01/thermal_zone/temp') is True:
                func = lambda: open('/sys/devices/LNXSYSTM:00/LNXTHERM:00/LNXTHERM:01/thermal_zone/temp').read().strip().rstrip('000')
            elif os.path.exists('/sys/bus/acpi/devices/LNXTHERM:00/thermal_zone/temp') is True:
                func = lambda: open('/sys/bus/acpi/devices/LNXTHERM:00/thermal_zone/temp').read().strip().rstrip('000')
            elif os.path.exists('/proc/acpi/thermal_zone/THM0/temperature') is True:
                func = lambda: open('/proc/acpi/thermal_zone/THM0/temperature').read().strip().lstrip('temperature :').rstrip(' C')
            elif os.path.exists('/proc/acpi/thermal_zone/THRM/temperature') is True:
                func = lambda: open('/proc/acpi/thermal_zone/THRM/temperature').read().strip().lstrip('temperature :').rstrip(' C')
            elif os.path.exists('/proc/acpi/thermal_zone/THR1/temperature') is True:
                func = lambda: open('/proc/acpi/thermal_zone/THR1/temperature').read().strip().lstrip('temperature :').rstrip(' C')
        return func
    pass