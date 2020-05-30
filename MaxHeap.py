class MaxHeap:
    def __init__(self, content=[]):
        self.heap = content
        self.build_heap()

    def build_heap(self):
        for i in range(int(len(self.heap) / 2), 0, -1):
            self.sift_down(i)

    def insert(self, val):
        self.heap.append(val)
        self.sift_up(len(self.heap))

    def retrieve_max(self):
        return self.heap[0]

    def delete_max(self):
        self.heap[0] = self.heap[-1]
        self.heap = self.heap[:-1]
        self.sift_down(1)

    def sift_down(self, i, length=None):
        if length == None:
            length = len(self.heap)
        if i <= int(length / 2):
            if i == int(length / 2) and length % 2 == 0:
                if self.heap[2 * i - 1] >= self.heap[i - 1]:
                    self.heap[i - 1], self.heap[2 * i - 1] = self.heap[2 * i - 1], self.heap[i - 1]
                    self.sift_down(2 * i - 1, length)
            else:
                if self.heap[2 * i - 1] >= self.heap[i - 1] or self.heap[2 * i] >= self.heap[i - 1]:
                    if self.heap[2 * i] >= self.heap[2 * i - 1]:
                        self.heap[i - 1], self.heap[2 * i] = self.heap[2 * i], self.heap[i - 1]
                        self.sift_down(2 * i + 1, length)
                    else:
                        self.heap[i - 1], self.heap[2 * i - 1] = self.heap[2 * i - 1], self.heap[i - 1]
                        self.sift_down(2 * i, length)

    def sift_up(self, i):
        if int(i / 2) - 1 >= 0:
            if self.heap[int(i / 2) - 1] < self.heap[i - 1]:
                self.heap[int(i / 2) - 1], self.heap[i - 1] = self.heap[i - 1], self.heap[int(i / 2) - 1]
                self.sift_up(int(i / 2))

    def show(self):
        print(self.heap)


if __name__ == "__main__":
    h1 = MaxHeap([6, 4, 9, 7, 6, 10, 1, 5, 2, 3])
    h1.show()
    h1.insert(8)
    h1.show()
    h2 = MaxHeap([6, 4, 9, 7, 6, 10, 1, 5, 2, 3])
    h2.delete_max()
    h2.show()