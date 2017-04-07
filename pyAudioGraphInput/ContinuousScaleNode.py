import pyAudioGraph as ag
import numpy as np
from . import continuous_mappings as contmap


class ContinuousScaleNode(ag.Node):
    """
    w_in and w_in_snap are control rate continuous [0, 1]
    w_f0 outputs f0
    """

    def __init__(self, world, A440=440):
        super().__init__(world)
        self.A440 = A440
        self.w_in = ag.InWire(self)
        self.w_in_snap = ag.InWire(self)
        self.w_in_scale = ag.ObjInWire(self, list(range(12)))
        self.w_f0 = ag.OutWire(self)

        self.prev_scale = []

        self.in_wires.extend([self.w_in, self.w_in_snap, self.w_in_scale])
        self.out_wires.append(self.w_f0)

    def set_A440(self, A440):
        self.A440 = A440

    def add_prev_scale(self, scale):
        for i in self.prev_scale:
            if(all([(abs(i - is_) > 1) and (12 - abs(i - is_) > 1) for is_ in scale])):
                scale.append(i)
        return sorted(scale)

    def calc_func(self):
        scale = self.w_in_scale.get_data()
        # scale = self.add_prev_scale(scale)
        scale = np.array(scale, dtype=np.int)
        offset = scale[0]
        edges = np.concatenate((scale - offset, [12])).astype(np.float)
        in_ = self.w_in.get_data()
        in_snap = self.w_in_snap.get_data()
        snap = 8 + in_snap * (100 - 8)  # meaningful range for snapping

        pwlx = contmap.pwlinear_with_xedges(edges)  # warp pitches to integers (notes in the scale)
        fn = contmap.replicate(contmap.weighted_sigmoid(snap))  # smooth step function
        fn = contmap.compose2(fn, pwlx)

        pwly = contmap.pwlinear_with_yedges(edges)  # warp back integers to pitches
        fn = contmap.compose2(pwly, fn)

        fn = contmap.replicate(fn, 12, 12)  # replicate for each octave

        in_ = (30 + in_ * (50))  # meaningful range of pitches
        out_pitch = fn(in_ - offset) + offset
        out_f0 = self.A440 * np.power(2, ((out_pitch - 69) / 12.0))
        self.w_f0.set_data(out_f0)
        self.prev_scale = scale
