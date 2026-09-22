# 3525. Find X Value of Array II

# You are given an array of positive integers nums and a positive integer k. You are also given a 2D array queries, where queries[i] = [indexi, valuei, starti, xi].

# You are allowed to perform an operation once on nums, where you can remove any suffix from nums such that nums remains non-empty.

# The x-value of nums for a given x is defined as the number of ways to perform this operation so that the product of the remaining elements leaves a remainder of x modulo k.

# For each query in queries you need to determine the x-value of nums for xi after performing the following actions:

# Update nums[indexi] to valuei. Only this step persists for the rest of the queries.
# Remove the prefix nums[0..(starti - 1)] (where nums[0..(-1)] will be used to represent the empty prefix).
# Return an array result of size queries.length where result[i] is the answer for the ith query.

# A prefix of an array is a subarray that starts from the beginning of the array and extends to any point within it.

# A suffix of an array is a subarray that starts at any point within the array and extends to the end of the array.

# Note that the prefix and suffix to be chosen for the operation can be empty.

# Note that x-value has a different definition in this version.

 

# Example 1:

# Input: nums = [1,2,3,4,5], k = 3, queries = [[2,2,0,2],[3,3,3,0],[0,1,0,1]]

# Output: [2,2,2]

# Explanation:

# For query 0, nums becomes [1, 2, 2, 4, 5], and the empty prefix must be removed. The possible operations are:
# Remove the suffix [2, 4, 5]. nums becomes [1, 2].
# Remove the empty suffix. nums becomes [1, 2, 2, 4, 5] with a product 80, which gives remainder 2 when divided by 3.
# For query 1, nums becomes [1, 2, 2, 3, 5], and the prefix [1, 2, 2] must be removed. The possible operations are:
# Remove the empty suffix. nums becomes [3, 5].
# Remove the suffix [5]. nums becomes [3].
# For query 2, nums becomes [1, 2, 2, 3, 5], and the empty prefix must be removed. The possible operations are:
# Remove the suffix [2, 2, 3, 5]. nums becomes [1].
# Remove the suffix [3, 5]. nums becomes [1, 2, 2].
# Example 2:

# Input: nums = [1,2,4,8,16,32], k = 4, queries = [[0,2,0,2],[0,2,0,1]]

# Output: [1,0]

# Explanation:

# For query 0, nums becomes [2, 2, 4, 8, 16, 32]. The only possible operation is:
# Remove the suffix [2, 4, 8, 16, 32].
# For query 1, nums becomes [2, 2, 4, 8, 16, 32]. There is no possible way to perform the operation.
# Example 3:

# Input: nums = [1,1,2,1,1], k = 2, queries = [[2,1,0,1]]

# Output: [5]

 

# Constraints:

# 1 <= nums[i] <= 10^9
# 1 <= nums.length <= 10^5
# 1 <= k <= 5
# 1 <= queries.length <= 2 * 10^4
# queries[i] == [indexi, valuei, starti, xi]
# 0 <= indexi <= nums.length - 1
# 1 <= valuei <= 10^9
# 0 <= starti <= nums.length - 1
# 0 <= xi <= k - 1


# Solution:



class Solution:
    def __init__(self):
        self.n = 0
        self.k = 0
        self.p = []
        self.c = []
        self.a = []

    def mg(self, nd):
        l = 2 * nd
        r = 2 * nd + 1

        self.p[nd] = (self.p[l] * self.p[r]) % self.k

        for i in range(self.k):
            t = (i * self.p[l]) % self.k

            for j in range(self.k):
                self.c[nd][i * self.k + j] = (
                    self.c[l][i * self.k + j]
                    + self.c[r][t * self.k + j]
                )

    def leaf(self, nd, v):
        self.c[nd] = [0] * (self.k * self.k)

        self.p[nd] = v % self.k

        for i in range(self.k):
            self.c[nd][
                i * self.k + (i * self.p[nd]) % self.k
            ] = 1

    def bld(self, nd, l, r):
        if l == r:
            self.leaf(nd, self.a[l])
            return

        m = (l + r) // 2

        self.bld(2 * nd, l, m)
        self.bld(2 * nd + 1, m + 1, r)

        self.mg(nd)

    def upd(self, nd, l, r, i, v):
        if l == r:
            self.leaf(nd, v)
            return

        m = (l + r) // 2

        if i <= m:
            self.upd(2 * nd, l, m, i, v)
        else:
            self.upd(2 * nd + 1, m + 1, r, i, v)

        self.mg(nd)

    def qry(self, nd, l, r, ql, st, res):

        # Segment is completely before query range
        if r < ql:
            return st

        # Segment is completely inside query range
        if l >= ql:
            for j in range(self.k):
                res[j] += self.c[nd][st * self.k + j]

            st = (st * self.p[nd]) % self.k

            return st

        m = (l + r) // 2

        # Query left first because order matters
        st = self.qry(
            2 * nd,
            l,
            m,
            ql,
            st,
            res
        )

        # Then query right
        st = self.qry(
            2 * nd + 1,
            m + 1,
            r,
            ql,
            st,
            res
        )

        return st

    def resultArray(self, nums, kk, queries):
        self.n = len(nums)
        self.k = kk
        self.a = nums

        self.p = [0] * (4 * self.n)

        self.c = [
            [0] * (self.k * self.k)
            for _ in range(4 * self.n)
        ]

        self.bld(1, 0, self.n - 1)

        ans = []

        for query in queries:
            id, v, s, x = query

            # Update
            self.upd(
                1,
                0,
                self.n - 1,
                id,
                v
            )

            # Initial prefix/product state
            st = 1 % self.k

            # Answer counts
            res = [0] * self.k

            # Query [s, n-1]
            self.qry(
                1,
                0,
                self.n - 1,
                s,
                st,
                res
            )

            ans.append(res[x])

        return ans