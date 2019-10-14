__all__ = ['VectorField']


class VectorField:
    def __init__(self, distance_function_name: str, distance_threshold: float):
        self.distance_function_name = distance_function_name
        self.distance_threshold = distance_threshold
