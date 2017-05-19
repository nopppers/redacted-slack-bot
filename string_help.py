
# Returns the element of the list at the given index
# or an empty string if no such element exists
def elem_or_empty_string(lst, idx):
    if len(lst) > idx:
        return lst[idx]
    else:
        return ""

# Splits the passed string and returns the element at the given index
# or an empty string if no such element exists
def split_elem_or_empty_string(str, idx, *splitArgs, **kwSplitArgs):
    return elem_or_empty_string(str.split(*splitArgs, **kwSplitArgs), idx)

# Partitions the passed string and returns the element at the given index
# or an empty string if no such element exists
def partition_elem_or_empty_string(str, idx, *partitionArgs, **kwPartitionArgs):
    return elem_or_empty_string(str.partition(*partitionArgs, **kwPartitionArgs), idx)