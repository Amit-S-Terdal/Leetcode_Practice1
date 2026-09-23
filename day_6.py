# 1658. Minimum Operations to Reduce X to Zero

# You are given an integer array nums and an integer x. In one operation, you can either remove the leftmost or the rightmost element from the array nums and subtract its value from x. Note that this modifies the array for future operations.

# Return the minimum number of operations to reduce x to exactly 0 if it is possible, otherwise, return -1.

 

# Example 1:

# Input: nums = [1,1,4,2,3], x = 5
# Output: 2
# Explanation: The optimal solution is to remove the last two elements to reduce x to zero.
# Example 2:

# Input: nums = [5,6,7,8,9], x = 4
# Output: -1
# Example 3:

# Input: nums = [3,2,20,1,1,3], x = 10
# Output: 5
# Explanation: The optimal solution is to remove the last three elements and the first two elements (5 operations in total) to reduce x to zero.
 

# Constraints:

# 1 <= nums.length <= 10^5
# 1 <= nums[i] <= 10^4
# 1 <= x <= 10^9



# Solution: 



class Solution:
    @staticmethod
    def minOperations(nums, x):
        n = len(nums)
        prefix = nums[0]
        sz = n

        for i in range(1, n):
            if prefix > x:
                sz = i
                break
            prefix += nums[i]

        # impossible
        if sz == n and prefix < x:
            return -1

        # let prefix <= x
        prefix -= nums[sz - 1]
        idx = sz - 1
        ans = float('inf')

        if idx >= 0 and prefix == x:
            ans = sz - 1

        suffix = 0

        for j in range(n - 1, -1, -1):
            suffix += nums[j]

            while suffix + prefix > x and prefix > 0:
                idx -= 1
                prefix -= nums[idx]

                if suffix + prefix <= x:
                    break

            if suffix + prefix == x:
                ans = min(ans, (n - j) + idx)

            if suffix >= x:
                break

        return -1 if ans == float('inf') else ans