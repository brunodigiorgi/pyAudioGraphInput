import leapMotionController as lmc
import pyAudioGraph as ag
import numpy as np


class LeapMotionNode(ag.Node):

    def __init__(self, world):
        super().__init__(world)

        self.w_rhand = ag.OutWire(self)
        self.w_rhand_pos = [ag.OutWire(self) for i in range(3)]
        self.w_rhand_vel = [ag.OutWire(self) for i in range(3)]
        self.w_rhand_angle = ag.OutWire(self)
        self.w_rhand_fing2_angle = ag.OutWire(self)
        self.controller = lmc.LMController()
        self.connected = False
        self.initialized = False

        self.out_wires.extend([self.w_rhand] + self.w_rhand_pos + self.w_rhand_vel + [self.w_rhand_angle, self.w_rhand_fing2_angle])

    def on_init(self):
        self.initialized = True

    def on_connect(self):
        self.connected = True

    def on_disconnect(self):
        self.connected = False

    def on_exit(self):
        return

    def calc_func(self):
        hands = self.controller.frame()
        self.w_rhand.set_data(0)
        if(hands[1].detected):
            self.w_rhand.set_data(1)
            h = hands[1]
            self.w_rhand_pos[0].set_data(h.palm_position_normalized.x)
            self.w_rhand_pos[1].set_data(h.palm_position_normalized.y)
            self.w_rhand_pos[2].set_data(h.palm_position_normalized.z)

            palm_angle = np.arctan2(h.palm_normal.x, h.palm_normal.y)

            # renormalization
            if(palm_angle < 0):
                palm_angle += 2 * np.pi
            palm_angle = (palm_angle - 3.3) * .5
            self.w_rhand_angle.set_data(palm_angle)

            bone = h.fingers[2].bones[3]
            d = (bone.next_joint.array - bone.prev_joint.array)
            m_angle = np.arctan2(d[2], d[1])

            # renormalization
            if(m_angle < 0):
                m_angle += 2 * np.pi
            m_angle = (4.50 - m_angle)
            self.w_rhand_fing2_angle.set_data(m_angle)