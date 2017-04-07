import Leap
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
        self.listener = SampleListener(self)
        self.controller = Leap.Controller()
        self.connected = False
        self.initialized = False

        # Have the sample listener receive events from the controller
        self.controller.add_listener(self.listener)

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
        if(not self.initialized or not self.connected):
            return

        frame = self.controller.frame()

        try:

            self.w_rhand.set_data(0)
            for hand in frame.hands:
                if(hand.is_left):
                    continue

                self.w_rhand.set_data(1)
                interaction_box = frame.interaction_box
                palm_position = interaction_box.normalize_point(hand.palm_position, True)
                self.w_rhand_pos[0].set_data(palm_position.x)
                self.w_rhand_pos[1].set_data(palm_position.y)
                self.w_rhand_pos[2].set_data(palm_position.z)

                self.w_rhand_vel[0].set_data(abs(hand.palm_velocity.x) / 200.0)
                self.w_rhand_vel[1].set_data(hand.palm_velocity.y)
                self.w_rhand_vel[2].set_data(hand.palm_velocity.z)

                palm_angle = np.arctan2(hand.palm_normal.x, hand.palm_normal.y)
                if(palm_angle < 0):
                    palm_angle += 2 * np.pi

                # renormalization
                palm_angle -= 4.2
                self.w_rhand_angle.set_data(palm_angle)

                try:
                    for finger in hand.fingers:
                        if(finger.type != 2):
                            continue

                        bone = finger.bone(3)
                        d = (bone.next_joint - bone.prev_joint)
                        m_angle = np.arctan2(d.z, d.y)
                        if(m_angle < 0):
                            m_angle += 2 * np.pi
                        m_angle = (4.50 - m_angle)
                        self.w_rhand_fing2_angle.set_data(m_angle)

                except SystemError:
                    continue

        except SystemError:
            pass


class SampleListener(Leap.Listener):

    def __init__(self, node):
        super().__init__()
        self.node = node

    def on_init(self, controller):
        self.node.on_init()

    def on_connect(self, controller):
        self.node.on_connect()

    def on_disconnect(self, controller):
        self.node.on_disconnect()

    def on_exit(self, controller):
        self.node.on_exit()
