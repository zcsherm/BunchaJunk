# Prob1
# Addstart. Get the sentinel node and the node it points to, point the sentinel to the new node, and the new node to the old node
pointer_1 = self._head.next
new_node = node(value,pointer_1)
self._head.next= node(value,self._head.next())

# prob2
# Addemd. Traverse the list until next is none, change that pointer to the new node
node = self._head()
while node.next:
  node = node.next
node.next(Node(value))

# prob3
# insert at index. Traverse the list n+1 times (so 0 gets the sentinel) point that node to the new node, and the new node to the pointer of that node
node = self._head()
for step in range(n)
  node = node.next
node.next = node(value, node.next)

# prob4
# remove at index. Traverse the list n+2 times (so 0 will get the 0th element [sentinel, 0,1...]) change the pointer of the previous node to the next of this one
node = self._head()
next_node = node.next
for step in range(n-1):
  node = node.next
  next_node = next_node.next  # This will have the node to be deleted
node.next =  next_node.next  # the previous node will change its next pointer to the node after the one we delete.

# prob5
# Remove value, traverse the list, saving the previous node each step too. if the current ode matches the value, point the previous to the next.
node = self._head()
next_node = node.next
while next_node.next:                              
  node = next_node
  next_node = node.next
  if next_node.data == value:
    node.next = next_node.next 
    return True
return False

# prob6
# count. Traverse the list and count elements
node = self._head()
count = 0
while node.next:
  node = node.next
  if node.data == value:
    count += 1
return count

#prob7
# find. Traverse the list and return true if element is found.
node = self._head
while node.next:
  node = node.next
  if node.data == value:
    return True
return False
  
# prob8
# Slice: Create a new list. Iterate through the first list until you get the first element of the slice. Make a new node that contains that data, point the previous node (sentinel) to it.
slice = sll()
slice_node = sll._head
node = self._head
# opting to raise the error at the end in stead of before looping
# rationale being that we have would to iterate through the list anyway to determine if the slice is in bounds
# This consumes more space, since we create the slice even if the requested size is oob. However, it means not needing to iterate more than once.
# If space was a concern we could instead call range first and compare the slice size before allocating memory to the new linked list.
lowerbound = start_
upperbound = start_index + (size-1)
counter = 0
while node.next and counter < upperbound:
  node = node.next
  if lowerbound <= counter <= upperbound:
    slice_node.next = Node(node.data)
  counter += 1
if counter < upperbound or counter < lowerbound:
  raise error
return slice
