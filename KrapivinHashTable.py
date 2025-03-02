import random

class KrapivinHashTable:
    def __init__(self, capacity=16):
        self.capacity = capacity
        self.table = [None] * capacity
        self.size = 0
        self.hash_functions = [
            lambda key, i, capacity: (hash(key) + i * (hash(key) // capacity + 1)) % capacity,  # Example: double hashing
            lambda key, i, capacity: (hash(key) + i**2) % capacity # Example quadratic probing
        ]

    def _hash(self, key, i, capacity):
        # Using a sequence of hash functions (example: double hashing + quadratic)
        return self.hash_functions[i % len(self.hash_functions)](key, i, capacity)

    def _find_slot(self, key):
        """Finds an empty slot or the slot with the key."""
        for i in range(self.capacity):
            index = self._hash(key, i, self.capacity)
            if self.table[index] is None or self.table[index][0] == key:
                return index, i
        return None, None # Table full

    def insert(self, key, value):
        """Inserts a key-value pair into the hash table."""
        if self.size >= self.capacity * 0.75: # Load factor
            self._resize()

        index, _ = self._find_slot(key)
        if index is None:
            return False # Table full

        if self.table[index] is None:
            self.table[index] = (key, value)
            self.size += 1
            return True
        else:
            self.table[index] = (key, value) # update existing key
            return True

    def get(self, key):
        """Retrieves the value associated with a key."""
        for i in range(self.capacity):
            index = self._hash(key, i, self.capacity)
            if self.table[index] is None:
                return None # Key not found
            if self.table[index][0] == key:
                return self.table[index][1]
        return None # Key not found

    def delete(self, key):
        """Deletes a key-value pair from the hash table."""
        for i in range(self.capacity):
             index = self._hash(key, i, self.capacity)
             if self.table[index] is None:
                return False # Key not found
             if self.table[index][0] == key:
                self.table[index] = None
                self.size -= 1
                return True
        return False

    def _resize(self):
        """Resizes the hash table when it becomes too full."""
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0
        for item in old_table:
            if item is not None:
                self.insert(item[0], item[1])

# Example usage:

ht = KrapivinHashTable()
ht.insert("apple", 1)
ht.insert("banana", 2)
ht.insert("cherry", 3)

print(ht.get("banana")) # Output: 2
print(ht.get("grape"))  # Output: None

ht.insert("apple", 4) # Update apple
print(ht.get("apple")) #Output: 4

ht.delete("banana")
print(ht.get("banana")) #output: None

#Demonstrate hash collision resolution.
for i in range(20):
    ht.insert(str(i), i)

print(ht.get('15'))
