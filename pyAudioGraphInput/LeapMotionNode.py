import leapMotionController as lmc
import pyAudioGraph as ag
import numpy as np


class LMVector:

    def __init__(self, parent):
        self.parent = parent
        self.x = ag.OutWire(parent)
        self.y = ag.OutWire(parent)
        self.z = ag.OutWire(parent)
        self.array = np.zeros((3,), dtype=np.float32)

    def set_data(self, other):
        self.x.set_data(other.x)
        self.y.set_data(other.y)
        self.z.set_data(other.z)
        self.array[0] = other.x
        self.array[1] = other.y
        self.array[2] = other.z


class LMBone:

    def __init__(self, parent):
        self.parent = parent
        self.prev_joint = LMVector(parent)
        self.next_joint = LMVector(parent)


class LMFinger:

    def __init__(self, parent):
        self.parent = parent
        self.bones = [LMBone(parent) for _ in range(lmc.NBONES)]


class LMHand:

    def __init__(self, parent):
        self.parent = parent
        self.is_valid = ag.OutWire(parent)
        self.detected = ag.OutWire(parent)
        self.palm_position = LMVector(parent)
        self.palm_velocity = LMVector(parent)
        self.palm_normal = LMVector(parent)
        self.palm_position_normalized = LMVector(parent)
        self.fingers = [LMFinger(parent) for _ in range(lmc.NFINGERS)]


class LeapMotionNode(ag.Node):

    def __init__(self, world):
        super().__init__(world)

        self.w_hands = [LMHand(self) for _ in range(lmc.NHANDS)]
        self.w_connected = ag.OutWire(self)
        self.w_has_focus = ag.OutWire(self)
        self.controller = lmc.LMController()

    def calc_func(self):
        self.w_connected.set_data(self.controller.isConnected())
        self.w_has_focus.set_data(self.controller.hasFocus())

        hands = self.controller.frame()
        for sh, oh in zip(self.w_hands, hands):
            sh.is_valid.set_data(oh.is_valid)
            sh.detected.set_data(oh.detected)
            sh.palm_position.set_data(oh.palm_position)
            sh.palm_velocity.set_data(oh.palm_velocity)
            sh.palm_normal.set_data(oh.palm_normal)
            sh.palm_position_normalized.set_data(oh.palm_position_normalized)
            for sf, of in zip(sh.fingers, oh.fingers):
                for sb, ob in zip(sf.bones, of.bones):
                    sb.prev_joint.set_data(ob.prev_joint)
                    sb.next_joint.set_data(ob.next_joint)