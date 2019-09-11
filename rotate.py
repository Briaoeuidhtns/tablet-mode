#!/usr/bin/env python3

from enum import Enum
from pydbus import SessionBus
from libinput import LibInput
from libinput.constant import SwitchState, Event


class Xrandr:
    __NAME = 'org.cinnamon.SettingsDaemon.XRANDR_2'
    __PATH = '/org/cinnamon/SettingsDaemon/XRANDR'

    class ROTATION(Enum):
        _NEXT = 0
        _0 = 1 << 0
        _90 = 1 << 1
        _180 = 1 << 2
        _270 = 1 << 3

    def __init__(self):
        bus = SessionBus()
        self.__xrandr = bus.get(self.__NAME, self.__PATH)

    def rotate(self, r: 'Xrandr.Rotation'):
        if r is Xrandr.ROTATION._NEXT:
            self.__xrandr.Rotate(0)
        else:
            self.__xrandr.RotateTo(r.value, 0)


class TabletMode:
    def __init__(self, device_path='/dev/input/event7'):
        self.__li = LibInput()
        self.__li.path_add_device(device_path)

    def event_stream(self):
        return (e.get_switch_event().get_switch_state() is SwitchState.ON
                for e in self.__li.get_event()
                if e.type is Event.SWITCH_TOGGLE)


if __name__ == '__main__':
    xrandr = Xrandr()
    tablet_mode = TabletMode()

    for is_tablet_mode in tablet_mode.event_stream():
        rotation = (Xrandr.ROTATION._270 if is_tablet_mode
                    else Xrandr.ROTATION._0)
        xrandr.rotate(rotation)
