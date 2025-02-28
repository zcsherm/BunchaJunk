# Name: Zachary Sherman
# OSU Email: Sherzach@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Project 2 Dynamic arrays
# Due Date: 02/03/2025
# Description: Implements a dynamic array into python using only static arrays as a given data element. Introduces
# Several important functions and methods including a resize, merge, remove, and slicing.


from static_array import StaticArray


class DynamicArrayException(Exception):
    """
    Custom exception class to be used by Dynamic Array
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class DynamicArray:
    def __init__(self, start_array=None):
        """
        Initialize new dynamic array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._size = 0
        self._capacity = 4
        self._data = StaticArray(self._capacity)

        # populate dynamic array with initial values (if provided)
        # before using this feature, implement append() method
        if start_array is not None:
            for value in start_array:
                self.append(value)

    def __str__(self) -> str:
        """
        Return content of dynamic array in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "DYN_ARR Size/Cap: "
        out += str(self._size) + "/" + str(self._capacity) + ' ['
        out += ', '.join([str(self._data[_]) for _ in range(self._size)])
        return out + ']'

    def __iter__(self):
        """
        Create iterator for loop
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        try:
            value = self[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index += 1
        return value

    def get_at_index(self, index: int) -> object:
        """
        Return value from given index position
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        return self._data[index]

    def set_at_index(self, index: int, value: object) -> None:
        """
        Store value at given index in the array
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        self._data[index] = value

    def __getitem__(self, index) -> object:
        """
        Same functionality as get_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.get_at_index(index)

    def __setitem__(self, index, value) -> None:
        """
        Same functionality as set_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.set_at_index(index, value)

    def is_empty(self) -> bool:
        """
        Return True is array is empty / False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size == 0

    def length(self) -> int:
        """
        Return number of elements stored in array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return the capacity of the array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    def print_da_variables(self) -> None:
        """
        Print information contained in the dynamic array.
        Used for testing purposes.
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        print(f"Length: {self._size}, Capacity: {self._capacity}, {self._data}")


    # -----------------------------------------------------------------------

    def resize(self, new_capacity: int) -> None:
        """
        Resizes the dynamic array to a new capacity. Invalid capacities include negative capacities or ones smaller
        than the current number of elements
        :param new_capacity: A positive integer
        """
        # Check if the capacity is valid
        if new_capacity <= 0:
            return
        if new_capacity < self.length():
            return

        new_array = StaticArray(new_capacity)
        # Copy over the data to the new array
        for index in range(self.length()):
            new_array[index]=self._data[index]

        # update private data members
        self._data = new_array
        self._capacity = new_capacity

    def append(self, value: object) -> None:
        """
        Appends a new value to the end of the dynamic array, resizing as needed
        :param value: The value to be appended
        """
        # Double the size of the array if we are out of space
        if self._capacity==self.length():
            self.resize(self._capacity * 2)
        self._size += 1
        self.set_at_index(self.length()-1,value)


    def insert_at_index(self, index: int, value: object) -> None:
        """
        Inserts a given value into the array at a given index.
        :param index: The index to be inserted at
        :param value: The value to be inserted
        """
        # Check if the index is negative or greater than the current size of the array.
        if index < 0 or index > self.length():
            raise DynamicArrayException

        # Resize if needed
        if self._capacity==self.length():
            self.resize(self._capacity*2)
        self._size += 1

        # Iterate through the list backwards, copying elements over so we can free a space for our insert
        for i in range(self.length()-1,index,-1):
            self.set_at_index(i,self.get_at_index(i-1))
        self.set_at_index(index, value)

    def dynArrayAddAt(self, index: int, value: object) -> None:
        # Check if the index is negative or greater than the current size of the array.
        if index < 0 or index > self.length():
            raise DynamicArrayException

        # Resize if needed
        if self._capacity==self.length():
            new_array = StaticArray(self._capacity*2)
            # Copy over the data to the new array
            for i in range(self.length()):

                new_array[i] = self._data[i]

            # update private data members
            self._data = new_array
            self._capacity = self._capacity*2
        self._size += 1

        # Iterate through the list backwards, copying elements over so we can free a space for our insert
        for i in range(self.length()-1,index,-1):
            self.set_at_index(i,self.get_at_index(i-1))
        self.set_at_index(index, value)

    def remove_at_index(self, index: int) -> None:
        """
        Deletes at en element in the dynamic array and fills in the elements into the empty space/
        :param index: The index of the element to delete
        """
        # Check that the index is not less than zero or greater than the current size of the array
        if index < 0 or index >= self.length():
            raise DynamicArrayException

        # If we have more than 3/4 of empty space in our array we must resize it down to 2 times the current number of
        # elements. Note that the size can never be less than 10.
        if self._capacity > self.length()*4 and self._capacity>10:
            if self.length()*2<10:
                resize_value = 10
            else:
                resize_value = self.length()*2
            self.resize(resize_value)

        # Copy all data over to fill in for the deleted entry
        for i in range(index,self.length()-1):
            self.set_at_index(i,self.get_at_index(i+1))
        self._size-=1


    def slice(self, start_index: int, size: int) -> "DynamicArray":
        """
        Returns a new dynamic array that is a 'slice' of the ariginal.
        :param start_index: The index to begin the slice on
        :param size: The size of the requested slice
        :return: A new dynamic array
        """
        # Check that the slice will not be OOB of our original index, and that the size is a positive integer
        end_index = start_index+size-1
        if end_index+1>self.length() or size<0 or start_index<0 or start_index>self.length()-1:
            raise DynamicArrayException

        # Move the corresponding data elements to our new array.
        new_array = DynamicArray()
        for offset in range(size):
            new_array.append(self.get_at_index(start_index+offset))
        return new_array

    def merge(self, second_da: "DynamicArray") -> None:
        """
        Merges a second dynamic array onto the current data array
        :param second_da: Another Dynamic Array.
        """
        # We can preserve order by doing a straight iteration and appending the values.
        for index in range(second_da.length()):
            self.append(second_da.get_at_index(index))

    def map(self, map_func) -> "DynamicArray":
        """
        Returns a new array that corresponds to the elements of the data array modified by a passed function
        :param map_func: A function to be applied element wise
        :return: A new dynamic array containing all the modified elements
        """
        new_array = DynamicArray()

        # Iterate through the original function and perform the function on each element, saving the result
        for index in range(self.length()):
            new_value = map_func(self.get_at_index(index))
            new_array.append(new_value)
        return new_array

    def filter(self, filter_func) -> "DynamicArray":
        """
        Returns a new dynamic array that contains the elements of the data array that pass a given filter function
        :param filter_func: The function to perform the filtering, must return a truthy condition to work properly
        :return: a new dynamic array that holds all elements that pass the filter
        """
        new_array = DynamicArray()

        # iterate through the current data and perfrom the filter element wise, saving the element if it passes.
        for index in range(self.length()):
            if filter_func(self.get_at_index(index)):
                new_array.append(self.get_at_index(index))
        return new_array

    def reduce(self, reduce_func, initializer=None) -> object:
        """
        Returns the result of the reduce_func across all elements. Performs arithmetic using 2 elements and carries
        the result forward across entire data array
        :param reduce_func: The function to be performed elementwise. The first variable being the accumulator
        :param initializer: The initial value to be used. Defaults to the first element of the array.
        :return: The result of the reduce_func.
        """
        start = 0
        # Set the initializer if it was not set
        if initializer is None:
            # Exits if there is no data
            if self.length()==0:
                return initializer
            initializer=self.get_at_index(0)
            start+=1

        # Iterate through the array and apply the function
        accumulator = initializer
        for index in range(start,self.length()):
            accumulator = reduce_func(accumulator,self.get_at_index(index))
        return accumulator


def find_mode(arr: DynamicArray) -> tuple:
    """
    Returns a tuple containing a dynamic array containing the modes of the dataset, and the frequency of said modes.
    Iterates through the array a single time for O(n) time complexity.
    :param arr: The given dynamic array
    :return:
    """
    # Start by initializing our array to return and setting up our variables
    new_array = DynamicArray()
    current_value = arr.get_at_index(0)         # The current value we are looking at
    current_value_frequency = 0                 # how often the current value has occured in the array
    current_mode_counter = 0                    # how many values are currently the mode
    max_mode_frequency=0                        # how much the mode has occured

    # Begin by iterating through the array
    for index in range(arr.length()):              # This feels wrong, however there is no getter function for size

        # As the passed array is sorted, if we are looking at a new value, then we should check if the previous
        # Value was a mode.
        if arr.get_at_index(index) != current_value:

            # Either the previous value had the same frequency as the existing mode, or it occurred more.
            if current_value_frequency==max_mode_frequency:
                # Append this value (or replace an existing value) into our return array at the appropriate space
                if current_mode_counter >= new_array.length():
                    new_array.append(current_value)
                else:
                    new_array.set_at_index(current_mode_counter,current_value)  # ie the third mode is index 2
                # Record that we have an additional value for the mode
                current_mode_counter += 1
            # If it occurred more then we can reset a lot of our variables
            elif current_value_frequency >max_mode_frequency:
                max_mode_frequency = current_value_frequency
                current_mode_counter = 1
                # Put this value into the first slot of the return array. Dont worry about clearing the array for now
                if new_array.length() != 0:
                    new_array.set_at_index(0,current_value)
                else:
                    new_array.append(current_value)
            # Update what the current value is
            current_value = arr.get_at_index(index)
            current_value_frequency = 1

        else:
            # We're seeing this number again so increase its frequency
            current_value_frequency += 1

    # Repeat the mode checking for the final value of the array, as this occurs outside the loop
    # Note that this is identical to what occurs in the above loop.
    if current_value_frequency == max_mode_frequency:
        if current_mode_counter>= new_array.length():
            new_array.append(current_value)
        else:
            new_array.set_at_index(current_mode_counter,current_value)
        current_mode_counter += 1
    elif current_value_frequency > max_mode_frequency:
        max_mode_frequency = current_value_frequency
        current_mode_counter = 1
        if new_array.length() != 0:
            new_array.set_at_index(0, current_value)
        else:
            new_array.append(current_value)

    # Now we have the modes front loaded onto our return array, but we may have extraneous elements after these
    # To solve this we simply slice our array to the number of elements that are the mode. Elegant.
    new_array = new_array.slice(0,current_mode_counter)
    return (new_array, max_mode_frequency)


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# resize - example 1")
    da = DynamicArray()

    # print dynamic array's size, capacity and the contents
    # of the underlying static array (data)
    da.print_da_variables()
    da.resize(8)
    da.print_da_variables()
    da.resize(2)
    da.print_da_variables()
    da.resize(0)
    da.print_da_variables()

    print("\n# resize - example 2")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8])
    print(da)
    da.resize(20)
    print(da)
    da.resize(4)
    print(da)
    da.resize(8)
    print(da)

    print("\n# append - example 1")
    da = DynamicArray()
    da.print_da_variables()
    da.append(1)
    da.print_da_variables()
    print(da)

    print("\n# append - example 2")
    da = DynamicArray()
    for i in range(9):
        da.append(i + 101)
        print(da)

    print("\n# append - example 3")
    da = DynamicArray()
    for i in range(600):
        da.append(i)
    print(da.length())
    print(da.get_capacity())

    print("\n# insert_at_index - example 1")
    da = DynamicArray([100])
    print(da)
    da.insert_at_index(0, 200)
    da.insert_at_index(0, 300)
    da.insert_at_index(0, 400)
    print(da)
    da.insert_at_index(3, 500)
    print(da)
    da.insert_at_index(1, 600)
    da.dynArrayAddAt(4, 66)
    print(da)

    print("\n# insert_at_index example 2")
    da = DynamicArray()
    try:
        da.insert_at_index(-1, 100)
    except Exception as e:
        print("Exception raised:", type(e))
    da.insert_at_index(0, 200)
    try:
        da.insert_at_index(2, 300)
    except Exception as e:
        print("Exception raised:", type(e))
    print(da)

    print("\n# insert at index example 3")
    da = DynamicArray()
    for i in range(1, 10):
        index, value = i - 4, i * 10
        try:
            da.insert_at_index(index, value)
        except Exception as e:
            print("Cannot insert value", value, "at index", index)
    print(da)

    print("\n# remove_at_index - example 1")
    da = DynamicArray([10, 20, 30, 40, 50, 60, 70, 80])
    print(da)
    da.remove_at_index(0)
    print(da)
    da.remove_at_index(6)
    print(da)
    da.remove_at_index(2)
    print(da)

    print("\n# remove_at_index - example 2")
    da = DynamicArray([1024])
    print(da)
    for i in range(17):
        da.insert_at_index(i, i)
    print(da.length(), da.get_capacity())
    for i in range(16, -1, -1):
        da.remove_at_index(0)
    print(da)

    print("\n# remove_at_index - example 3")
    da = DynamicArray()
    print(da.length(), da.get_capacity())
    [da.append(1) for i in range(100)]  # step 1 - add 100 elements
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(68)]  # step 2 - remove 68 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 3 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 4 - remove 1 element
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(14)]  # step 5 - remove 14 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 6 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 7 - remove 1 element
    print(da.length(), da.get_capacity())

    for i in range(14):
        print("Before remove_at_index(): ", da.length(), da.get_capacity(), end="")
        da.remove_at_index(0)
        print(" After remove_at_index(): ", da.length(), da.get_capacity())

    print("\n# remove at index - example 4")
    da = DynamicArray([1, 2, 3, 4, 5])
    print(da)
    for _ in range(5):
        da.remove_at_index(0)
        print(da)

    print("\n# slice example 1")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8, 9])
    da_slice = da.slice(1, 3)
    print(da, da_slice, sep="\n")
    da_slice.remove_at_index(0)
    print(da, da_slice, sep="\n")

    print("\n# slice example 2")
    da = DynamicArray([10, 11, 12, 13, 14, 15, 16])
    print("SOURCE:", da)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1), (6, -1)]
    for i, cnt in slices:
        print("Slice", i, "/", cnt, end="")
        try:
            print(" --- OK: ", da.slice(i, cnt))
        except:
            print(" --- exception occurred.")

    print("\n# merge example 1")
    da = DynamicArray([1, 2, 3, 4, 5])
    da2 = DynamicArray([10, 11, 12, 13])
    print(da)
    da.merge(da2)
    print(da)

    print("\n# merge example 2")
    da = DynamicArray([1, 2, 3])
    da2 = DynamicArray()
    da3 = DynamicArray()
    da.merge(da2)
    print(da)
    da2.merge(da3)
    print(da2)
    da3.merge(da)
    print(da3)

    print("\n# map example 1")
    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    print(da.map(lambda x: x ** 2))

    print("\n# map example 2")


    def double(value):
        return value * 2


    def square(value):
        return value ** 2


    def cube(value):
        return value ** 3


    def plus_one(value):
        return value + 1


    da = DynamicArray([plus_one, double, square, cube])
    for value in [1, 10, 20]:
        print(da.map(lambda x: x(value)))

    print("\n# filter example 1")


    def filter_a(e):
        return e > 10


    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    result = da.filter(filter_a)
    print(result)
    print(da.filter(lambda x: (10 <= x <= 20)))

    print("\n# filter example 2")


    def is_long_word(word, length):
        return len(word) > length


    da = DynamicArray("This is a sentence with some long words".split())
    print(da)
    for length in [3, 4, 7]:
        print(da.filter(lambda word: is_long_word(word, length)))

    print("\n# reduce example 1")
    values = [100, 5, 10, 15, 20, 25]
    da = DynamicArray(values)
    print(da)
    print(da.reduce(lambda x, y: (x // 5 + y ** 2)))
    print(da.reduce(lambda x, y: (x + y ** 2), -1))

    print("\n# reduce example 2")
    da = DynamicArray([100])
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))
    da.remove_at_index(0)
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))

    print("\n# find_mode - example 1")
    test_cases = (
        [1, 1, 2, 3, 3, 4],
        [1, 2, 3, 4, 5],
        ["Apple", "Banana", "Banana", "Carrot", "Carrot",
         "Date", "Date", "Date", "Eggplant", "Eggplant", "Eggplant",
         "Fig", "Fig", "Grape"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}\n")

    case = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    da = DynamicArray()
    for x in range(len(case)):
        da.append(case[x])
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}")
