import streamlit as st

# Base class for hashing algorithms
class HashingAlgorithm:
    def __init__(self):
        self.buckets = [[]]
        self.load_factor_threshold = 1.0

    def insert(self, key):
        raise NotImplementedError

    def delete(self, key):
        raise NotImplementedError

    def set_load_factor(self, load_factor):
        self.load_factor_threshold = load_factor

    def reset_buckets(self):
        self.buckets = [[]]

# Extendible Hashing
class ExtendibleHashing(HashingAlgorithm):
    def __init__(self):
        super().__init__()
        self.global_depth = 1
        self.buckets = [[] for _ in range(2 ** self.global_depth)]
        self.local_depths = [1] * (2 ** self.global_depth)

    def _split(self, index):
        local_depth = self.local_depths[index]
        if local_depth >= self.global_depth:
            self.global_depth += 1
            # Create new buckets
            new_buckets = [[] for _ in range(2 ** self.global_depth)]
            # Copy existing elements to new buckets
            for i in range(len(self.buckets)):
                new_index = i % (2 ** self.global_depth)
                new_buckets[new_index] = self.buckets[i]

            self.buckets = new_buckets
            self.local_depths.extend([local_depth] * (2 ** (self.global_depth - 1)))

        new_index = index ^ (1 << local_depth)
        self.local_depths[new_index] = local_depth + 1
        self.local_depths[index] = local_depth + 1

        keys_to_redistribute = self.buckets[index][:]
        self.buckets[index] = []
        for key in keys_to_redistribute:
            self.insert(key)

    def insert(self, key):
        index = key % (2 ** self.global_depth)
        self.buckets[index].append(key)

        if len(self.buckets[index]) > (2 ** self.local_depths[index]):
            self._split(index)

    def delete(self, key):
        index = key % (2 ** self.global_depth)
        if key in self.buckets[index]:
            self.buckets[index].remove(key)

    def print_depths(self):
        return f"Local Depths: {self.local_depths}"

    def display_buckets(self):
        bucket_info = {}
        for i, bucket in enumerate(self.buckets):
            # Convert index to binary format
            bucket_index_binary = format(i, f'0{self.global_depth}b')  # Universal form for extendible hashing
            bucket_info[bucket_index_binary] = bucket
        return bucket_info

# Linear Hashing
class LinearHashing(HashingAlgorithm):
    def __init__(self):
        super().__init__()
        self.next_split = 0
        self.level = 1
        self.buckets = [[] for _ in range(2 ** self.level)]

    def insert(self, key):
        index = key % (2 ** self.level)
        if index < self.next_split:
            index = key % (2 ** (self.level + 1))

        self.buckets[index].append(key)

        if len(self.buckets[self.next_split]) > self.load_factor_threshold * (2 ** self.level):
            self._split()

    def _split(self):
        self.buckets.append([])
        keys_to_redistribute = self.buckets[self.next_split][:]
        self.buckets[self.next_split] = []

        for key in keys_to_redistribute:
            index = key % (2 ** (self.level + 1))
            self.buckets[index].append(key)

        self.next_split += 1
        if self.next_split >= (2 ** self.level):
            self.level += 1
            self.next_split = 0

    def delete(self, key):
        index = key % (2 ** self.level)
        if index < self.next_split:
            index = key % (2 ** (self.level + 1))
        if key in self.buckets[index]:
            self.buckets[index].remove(key)

# Bitmap Hashing
class BitmapHashing(HashingAlgorithm):
    def __init__(self, size):
        super().__init__()
        self.size = size
        self.bitmap = [0] * self.size
        self.keys = []  # Store inserted keys
        self.bitmaps_history = []  # Store bitmap after each insertion

    def insert(self, key):
        index = key % self.size
        self.bitmap[index] = 1
        self.keys.append(key)  # Store the key
        self.bitmaps_history.append(self.bitmap.copy())  # Store a copy of the bitmap
        return self.bitmap  # Return the current bitmap

    def delete(self, key):
        index = key % self.size
        if key in self.keys:
            self.bitmap[index] = 0
            self.keys.remove(key)

    def reset_buckets(self):
        self.bitmap = [0] * self.size
        self.keys = []
        self.bitmaps_history = []  # Clear stored bitmap history

    def display(self):
        return self.bitmap

    def display_history(self):
        return self.bitmaps_history

# Initialize Streamlit app
st.title("Hashing Algorithm Simulator")

# Sidebar selection for hashing method
hashing_method = st.sidebar.selectbox(
    "Select Hashing Method", 
    ["Extendible Hashing", "Linear Hashing", "Bitmap Hashing"]
)

# Load Factor input for Linear Hashing only
if hashing_method == "Linear Hashing":
    load_factor_input = st.sidebar.number_input(
        "Set Load Factor Threshold for Linear Hashing", 
        min_value=0.1, max_value=1.0, value=0.7, step=0.1
    )

# Bitmap size input
bitmap_size_input = st.sidebar.number_input(
    "Set Bitmap Size", 
    min_value=1, value=8, step=1
)

# Initialize the selected hashing algorithm
if 'hash_algo' not in st.session_state or st.session_state.hashing_method != hashing_method:
    if hashing_method == "Extendible Hashing":
        st.session_state.hash_algo = ExtendibleHashing()
    elif hashing_method == "Linear Hashing":
        st.session_state.hash_algo = LinearHashing()
    elif hashing_method == "Bitmap Hashing":
        st.session_state.hash_algo = BitmapHashing(size=bitmap_size_input)
    st.session_state.hashing_method = hashing_method

# Allow user to update load factor (only for Linear Hashing)
if hashing_method == "Linear Hashing" and st.button("Update Load Factor Threshold"):
    st.session_state.hash_algo.set_load_factor(load_factor_input)
    st.write(f"Updated Load Factor Threshold to: {load_factor_input}")

# Allow user to update bitmap size
if hashing_method == "Bitmap Hashing" and st.button("Update Bitmap Size"):
    st.session_state.hash_algo = BitmapHashing(size=bitmap_size_input)  # Update bitmap size
    st.write(f"Updated Bitmap Size to: {bitmap_size_input}")

# Input key for inserting
key_to_insert = st.number_input("Enter Key to Insert", min_value=0, step=1)
if st.button("Insert Key"):
    updated_bitmap = st.session_state.hash_algo.insert(key_to_insert)
    st.write(f"Inserted Key: {key_to_insert}")

# Input key for deleting
key_to_delete = st.number_input("Enter Key to Delete", min_value=0, step=1)
if st.button("Delete Key"):
    st.session_state.hash_algo.delete(key_to_delete)
    st.write(f"Deleted Key: {key_to_delete}")

# Button to show buckets in binary format
if st.button("Show Buckets"):
    if hashing_method == "Bitmap Hashing":
        st.write("Bitmap History After Each Insertion:")
        for idx, bitmap in enumerate(st.session_state.hash_algo.display_history()):
            st.write(f"After Inserting Key {st.session_state.hash_algo.keys[idx]}: {bitmap}")
    else:
        st.write("Buckets (in binary):")
        bucket_info = st.session_state.hash_algo.display_buckets()
        for binary_index, bucket in bucket_info.items():
            st.write(f"Bucket {binary_index}: {bucket}")
        if hashing_method == "Extendible Hashing":
            st.write(st.session_state.hash_algo.print_depths())

# Button to reset bitmap
if hashing_method == "Bitmap Hashing":
    if st.button("Reset Bitmap"):
        st.session_state.hash_algo.reset_buckets()
        st.write("Bitmap has been reset.")
        st.write(f"Current Bitmap: {st.session_state.hash_algo.display()}")

# Button to reset/clear buckets
if st.button("Reset Buckets"):
    st.session_state.hash_algo.reset_buckets()
    if hashing_method == "Bitmap Hashing":
        st.write(f"Bitmap has been reset to: {st.session_state.hash_algo.display()}")
    else:
        st.write("Buckets have been reset.")

# Extendible Hashing = [5, 7, 12, 14, 3, 9, 21, 27, 18, 23]
# Linear Hashing = [3, 2, 4, 1, 8, 14, 5, 10, 7, 24, 17, 13, 15], load factor = 0.7
# Bitmap Hashing = [3, 5, 7, 10, 12, 15, 20, 22], bitmap size = 8