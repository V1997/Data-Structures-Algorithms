class LRU_Cache(object):
    def __init__(self, capacity):
        # Initialize class variables
        self.bucket_array = [None] * (capacity + 1)
        self.num_of_elements = 0
        self.queue = []
    def get(self, key):
        if len(self.bucket_array) == 1: #capacity is zero
            return -1
        # Retrieve item from provided key. Return -1 if nonexistent. 
        if key > len(self.bucket_array):
            return -1
        if self.bucket_array[key] != None:
            self.num_of_elements -=1 
            if self.queue[0] == key: 
                self.queue.append(self.queue.pop(0))
            return self.bucket_array[key]
        else:#collision
            return -1

    def set(self, key, value):
        if len(self.bucket_array) == 1:
            print("Warnning: cannot perform operations on 0 capacity cache")
            return
        # Set the value if the key is not present in the cache. If the cache is at capacity remove the oldest item. 
        if key < len(self.bucket_array) and  self.bucket_array[key] == None:
            self.bucket_array[key] = value
            self.num_of_elements += 1
            self.queue.append(key)
        else:#cache full
            oldest = self.queue.pop(0)
            self.bucket_array[oldest] = None
            self.bucket_array.extend([None])
            self.bucket_array[key] = value



#####TEST-1
print('------------------TEST-1--------------------')
cache = LRU_Cache(5)

cache.set(1, 1);
cache.set(2, 2);
cache.set(3, 3);
cache.set(4, 4);

print(cache.get(1))       # returns 1
print(cache.get(2))       # returns 2
print(cache.get(9))     # returns -1 because 9 is not present in the cache
cache.set(5, 5)
cache.set(6, 6)
print(cache.get(3))      # re -1 because the cache reached it's capacity and 3 was the least recently used entry


#####TEST-2: update a value for existing key and check whether it's reflecting properly or not.
print('------------------TEST-2--------------------')
our_cache = LRU_Cache(2)
our_cache.set(1, 1)
our_cache.set(2, 2)
our_cache.set(1, 10)
print(our_cache.get(1))
# should return 10
print(our_cache.get(2))
# should return 2

############TEST-3: edge cases
print('------------------TEST-3--------------------')
our_cache = LRU_Cache(0)
our_cache.set(1, 1)
# should print some warning message like "Can't perform operations on 0 capacity cache"
print(our_cache.get(1))
# should return -1