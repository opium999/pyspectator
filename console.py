import subprocess
import platform
from os import linesep
from time import sleep
from pyspectator.convert import UnitByte


clear_command = "cls" if platform.system() == "Windows" else "clear"


def clear():
    subprocess.call(clear_command, shell=True)


def print_hr(space_before=False, space_after=False):
    before = linesep if space_before else ''
    after = linesep if space_after else ''
    print(before + '-' * 80 + after)


class Format(object):

    @staticmethod
    def temperature(value):
        return str(value) + '°C'

    @staticmethod
    def byte_value(value):
        value, unit = UnitByte.auto_convert(value)
        value = '{0:.2f}'.format(value)
        unit = UnitByte.get_name_reduction(unit)
        return value + unit

    @staticmethod
    def percent(value):
        return str(value) + '%'


def start(computer):
    print('Start monitoring system...')
    print_hr(space_after=True)
    # Show system info for ~16 seconds
    for _ in range(16):
        clear()
        # Display general information about computer
        print('Hostname: ' + str(computer.hostname))
        print('OS: ' + str(computer.os))
        print('Boot time: ' + str(computer.boot_time))
        print('Uptime: ' + str(computer.uptime))
        # Display CPU info
        print('CPU name: ' + str(computer.processor.name))
        print('Amount of CPU cores: ' + str(computer.processor.count))
        print('CPU load: ' + Format.percent(computer.processor.percent))
        cpu_temperature = 'unknown'
        if computer.processor.temperature is not None:
            cpu_temperature = Format.temperature(computer.processor.temperature)
        print('CPU temperature: ' + cpu_temperature)
        # Display virtual memory info
        print('Virtual memory: use {0} from {1}, {2}'.format(
            Format.byte_value(computer.virtual_memory.available),
            Format.byte_value(computer.virtual_memory.total),
            Format.percent(computer.virtual_memory.percent)
        ))
        # Display nonvolatile memory info
        output_format1 = '{0:_^16}{1:_^16}{2:_^16}{3:_^16}{4:_^16}'
        output_format2 = '{0: ^16}{1: ^16}{2: ^16}{3: ^16}{4: ^16}'
        print(output_format1.format('Device', 'Total', 'Use', 'Type', 'Mount'))
        for dev in computer.nonvolatile_memory:
            output_text = output_format2.format(
                dev.device,
                Format.byte_value(dev.total),
                Format.percent(dev.percent),
                dev.fstype,
                dev.mountpoint
            )
            print(output_text)
        sleep(1)
    clear()
    # Output CPU statistic
    print('{0:_^26}_{1:_^26}_{2:_^26}'.format('Time', 'CPU load', 'CPU temperature'))
    percent_stats = computer.processor.percent_stats
    temperature_stats = computer.processor.temperature_stats
    count = max(len(percent_stats), len(temperature_stats))
    percent_stats_timetable = sorted(percent_stats)[0:count]
    temperature_stats_timetable = sorted(temperature_stats)[0:count]
    for percent_dtime, temperature_dtime in zip(percent_stats_timetable, temperature_stats_timetable):
        current_line = '{0: ^26} {1: ^26} {2: ^26}'.format(
            percent_dtime.strftime('%H:%M:%S'),
            Format.percent(percent_stats[percent_dtime]),
            Format.temperature(temperature_stats[temperature_dtime])
        )
        print(current_line)
    print_hr(space_before=True)
    print('Shutdown monitoring system...')