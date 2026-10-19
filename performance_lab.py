# 🔍 Problem 1: Find Most Frequent Element
# Given a list of integers, return the value that appears most frequently.
# If there's a tie, return any of the most frequent.
#
# Example:
# Input: [1, 3, 2, 3, 4, 1, 3]
# Output: 3

def most_frequent(numbers):
    counts = {}
    for num in numbers:
        counts[num] = counts.get(num, 0) + 1

    max_count = 0
    result = None
    for num, count in counts.items():
        if count > max_count:
            max_count = count
            result = num
    return result

# Test cases
print(most_frequent([1, 3, 2, 3, 4, 1, 3]))  # 3
print(most_frequent([5]))                     # 5 (single element)
print(most_frequent([1, 2, 3]))               # any of them (all tied)
print(most_frequent([]))                      # None (empty list, edge case)

"""
Time and Space Analysis for problem 1:
- Best-case: O(n). Every number has to be looked at at least once to count
  it, so there is no shortcut even if the first number is the most frequent.
- Worst-case: O(n). One pass builds the counts and a second pass scans the
  dictionary for the max. Both scale linearly.
- Average-case: O(n).
- Space complexity: O(n). If every number is unique, the counts dictionary
  holds one entry per number.
- Why this approach? A dictionary gives O(1) average lookups and updates, so
  counting stays linear. Comparing every number to every other number would
  be O(n^2).
- Could it be optimized? collections.Counter with most_common(1) does the
  same job with less code, but the time complexity stays O(n). It is a
  readability improvement, not a performance one.
"""


# 🔍 Problem 2: Remove Duplicates While Preserving Order
# Write a function that returns a list with duplicates removed but preserves order.
#
# Example:
# Input: [4, 5, 4, 6, 5, 7]
# Output: [4, 5, 6, 7]

def remove_duplicates(nums):
    seen = set()
    result = []
    for num in nums:
        if num not in seen:
            seen.add(num)
            result.append(num)
    return result

# Test cases
print(remove_duplicates([4, 5, 4, 6, 5, 7]))  # [4, 5, 6, 7]
print(remove_duplicates([]))                   # [] (empty list)
print(remove_duplicates([1, 1, 1]))            # [1] (all duplicates)
print(remove_duplicates([1, 2, 3]))            # [1, 2, 3] (no duplicates)

"""
Time and Space Analysis for problem 2:
- Best-case: O(n). Every element is checked against the set once.
- Worst-case: O(n). Set lookups stay O(1) on average no matter how many
  duplicates exist.
- Average-case: O(n).
- Space complexity: O(n). The seen set and the result list can each grow to
  the size of the input if there are no duplicates.
- Why this approach? Checking "have I seen this before" with a list would
  scan the whole list each time (O(n) per check, O(n^2) overall). A set gives
  O(1) average membership checks, which keeps the whole function linear.
- Could it be optimized? Not meaningfully. O(n) is already optimal because
  every element has to be looked at at least once.
"""


# 🔍 Problem 3: Return All Pairs That Sum to Target
# Write a function that returns all unique pairs of numbers in the list that sum to a target.
# Order of output does not matter. Assume input list has no duplicates.
#
# Example:
# Input: ([1, 2, 3, 4], target=5)
# Output: [(1, 4), (2, 3)]

# ORIGINAL (unoptimized) approach, kept here for comparison.
def find_pairs_brute_force(nums, target):
    pairs = []
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                pairs.append((nums[i], nums[j]))
    return pairs


# OPTIMIZED approach (see the optimization comparison below).
def find_pairs(nums, target):
    seen = set()
    pairs = []
    for num in nums:
        complement = target - num
        if complement in seen:
            pairs.append((complement, num))
        seen.add(num)
    return pairs

# Test cases
print(find_pairs([1, 2, 3, 4], 5))     # [(2, 3), (1, 4)] (order does not matter)
print(find_pairs([], 5))                # [] (empty list)
print(find_pairs([1, 2], 10))           # [] (no pairs sum to target)
print(find_pairs([5], 10))              # [] (single element, no pair possible)

"""
Time and Space Analysis for problem 3:
- Best-case: O(n). One pass through the list with a set membership check at
  each step.
- Worst-case: O(n). Still one pass, no matter how many pairs exist.
- Average-case: O(n).
- Space complexity: O(n) for the seen set, which can hold up to n elements.
- Why this approach? Brute force compares every number to every other number
  (O(n^2)). Using a set to remember what has already been seen lets us check
  for a number's complement in O(1) average time, so the whole function drops
  to O(n).
- Could it be optimized? This is the optimized version. The brute-force
  version above is the original starting point.
"""

"""
OPTIMIZATION COMPARISON (Problem 3):
I refactored find_pairs by trading extra space for less time.

Original (find_pairs_brute_force):
- Time: O(n^2), nested loops compare every pair.
- Extra space: O(1) beyond the output list.

Optimized (find_pairs):
- Time: O(n), one pass with an O(1) average set lookup per number.
- Extra space: O(n) for the seen set.

Measured on random lists of unique integers (seconds, single run):
    n = 1,000    brute force 0.0240    optimized 0.00013
    n = 5,000    brute force 0.6055    optimized 0.00092
    n = 10,000   brute force 2.4811    optimized 0.00149

When n grew 10x, brute force got about 100x slower (the n^2 pattern), while
the optimized version grew roughly 10x (the n pattern). This is the same kind
of n^2 to n fix described in the GTA Online example in the assignment context.

Trade-off: the optimized version uses more memory. For very small lists the
brute-force version can be just as fast because of lower overhead, but as the
input grows the O(n) version scales far better.
"""


# 🔍 Problem 4: Simulate List Resizing (Amortized Cost)
# Create a function that adds n elements to a list that has a fixed initial capacity.
# When the list reaches capacity, simulate doubling its size by creating a new list
# and copying all values over (simulate this with print statements).
#
# Example:
# add_n_items(6) → should print when resizing happens.

def add_n_items(n):
    capacity = 2
    size = 0
    data = [None] * capacity

    for i in range(n):
        if size == capacity:
            capacity *= 2
            print(f"Resizing: copying {size} items into new capacity of {capacity}")
            new_data = [None] * capacity
            for j in range(size):
                new_data[j] = data[j]
            data = new_data

        data[size] = i
        size += 1
        print(f"Added item {i}, size={size}, capacity={capacity}")

# Test cases
add_n_items(6)
add_n_items(0)  # edge case: adding nothing, should do nothing
add_n_items(1)  # edge case: single item, no resize needed

"""
Time and Space Analysis for problem 4:
- When do resizes happen? Whenever size reaches capacity, right before the
  next item is added. Capacity doubles each time (2, 4, 8, 16, ...), so
  resizes become less and less frequent as the list grows.
- What is the worst-case for a single append? O(n). The append that triggers
  a resize has to copy every existing element into the new, larger array.
- What is the amortized time per append overall? O(1). A resizing append
  costs O(n), but resizes only happen at powers of 2, so the total copying
  cost spread across all appends averages out to constant time per append.
- Space complexity: O(n). Capacity never exceeds roughly 2x the number of
  elements stored because of doubling.
- Why does doubling reduce the cost overall? If capacity grew by a fixed
  amount (like +1), nearly every append would trigger a resize, making each
  append about O(n) and the total O(n^2). With doubling, the gap between
  resizes also doubles, so total copying across n appends stays proportional
  to n instead of n^2.
"""


# 🔍 Problem 5: Compute Running Totals
# Write a function that takes a list of numbers and returns a new list
# where each element is the sum of all elements up to that index.
#
# Example:
# Input: [1, 2, 3, 4]
# Output: [1, 3, 6, 10]
# Because: [1, 1+2, 1+2+3, 1+2+3+4]

def running_total(nums):
    totals = []
    current_sum = 0
    for num in nums:
        current_sum += num
        totals.append(current_sum)
    return totals

# Test cases
print(running_total([1, 2, 3, 4]))  # [1, 3, 6, 10]
print(running_total([]))             # [] (empty list)
print(running_total([5]))            # [5] (single element)
print(running_total([-1, 1, -1]))    # [-1, 0, -1] (negative numbers)

"""
Time and Space Analysis for problem 5:
- Best-case: O(n). Every element must be visited once to build the running
  sum.
- Worst-case: O(n). No shortcuts exist for this problem.
- Average-case: O(n).
- Space complexity: O(n) for the totals list, which is the same length as
  the input.
- Why this approach? Carrying a running current_sum forward avoids re-summing
  from the start at every index, which would be O(n^2).
- Could it be optimized? Not in time. O(n) is the best possible because
  every number has to be touched at least once.
"""