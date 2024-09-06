import time
class CircularBuffer:
    def __init__(self, size):
        self.size = size
        self.buffer = [None] * size
        self.start = 0
        self.end = 0
        self.is_full = False

    def append(self, item):
        self.buffer[self.end] = item
        if self.is_full:
            self.start = (self.start + 1) % self.size
        self.end = (self.end + 1) % self.size
        self.is_full = self.end == self.start

    def get(self):
        if not self.is_full and self.end == self.start:
            return []
        if self.is_full:
            return self.buffer[self.start:] + self.buffer[:self.end]
        return self.buffer[self.start:self.end]

    def __repr__(self):
        return f'CircularBuffer({self.get()})'

# Example usage:
cb = CircularBuffer(10)
for i in range(10):
    cb.append(i)
    print(cb)
    time.sleep(1)

print(self)