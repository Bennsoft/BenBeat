class VisualMapping:
    def __init__(self, musical_value, scale=1.0, offset=0.0, smoothing_alpha=0.1):
        """
        :param musical_value: string, e.g., 'bass', 'mids', 'treble', 'frequency'
        :param scale: float, scaling factor
        :param offset: float, value to add after scaling
        :param smoothing_alpha: smoothing factor (closer to 0 = slower smoothing)
        """
        self.musical_value = musical_value
        self.scale = scale
        self.offset = offset
        self.smoothing_alpha = smoothing_alpha
        self.smoothed_value = 0.0

    def update(self, musical_data):
        raw_value = getattr(musical_data, self.musical_value)
        new_value = self.scale * raw_value + self.offset
        self.smoothed_value = (
            (1 - self.smoothing_alpha) * self.smoothed_value +
            self.smoothing_alpha * new_value
        )
        return self.smoothed_value
