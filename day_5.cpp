// 3525. Find X Value of Array II

// You are given an array of positive integers nums and a positive integer k. You are also given a 2D array queries, where queries[i] = [indexi, valuei, starti, xi].

// You are allowed to perform an operation once on nums, where you can remove any suffix from nums such that nums remains non-empty.

// The x-value of nums for a given x is defined as the number of ways to perform this operation so that the product of the remaining elements leaves a remainder of x modulo k.

// For each query in queries you need to determine the x-value of nums for xi after performing the following actions:

// Update nums[indexi] to valuei. Only this step persists for the rest of the queries.
// Remove the prefix nums[0..(starti - 1)] (where nums[0..(-1)] will be used to represent the empty prefix).
// Return an array result of size queries.length where result[i] is the answer for the ith query.

// A prefix of an array is a subarray that starts from the beginning of the array and extends to any point within it.

// A suffix of an array is a subarray that starts at any point within the array and extends to the end of the array.

// Note that the prefix and suffix to be chosen for the operation can be empty.

// Note that x-value has a different definition in this version.

 

// Example 1:

// Input: nums = [1,2,3,4,5], k = 3, queries = [[2,2,0,2],[3,3,3,0],[0,1,0,1]]

// Output: [2,2,2]

// Explanation:

// For query 0, nums becomes [1, 2, 2, 4, 5], and the empty prefix must be removed. The possible operations are:
// Remove the suffix [2, 4, 5]. nums becomes [1, 2].
// Remove the empty suffix. nums becomes [1, 2, 2, 4, 5] with a product 80, which gives remainder 2 when divided by 3.
// For query 1, nums becomes [1, 2, 2, 3, 5], and the prefix [1, 2, 2] must be removed. The possible operations are:
// Remove the empty suffix. nums becomes [3, 5].
// Remove the suffix [5]. nums becomes [3].
// For query 2, nums becomes [1, 2, 2, 3, 5], and the empty prefix must be removed. The possible operations are:
// Remove the suffix [2, 2, 3, 5]. nums becomes [1].
// Remove the suffix [3, 5]. nums becomes [1, 2, 2].
// Example 2:

// Input: nums = [1,2,4,8,16,32], k = 4, queries = [[0,2,0,2],[0,2,0,1]]

// Output: [1,0]

// Explanation:

// For query 0, nums becomes [2, 2, 4, 8, 16, 32]. The only possible operation is:
// Remove the suffix [2, 4, 8, 16, 32].
// For query 1, nums becomes [2, 2, 4, 8, 16, 32]. There is no possible way to perform the operation.
// Example 3:

// Input: nums = [1,1,2,1,1], k = 2, queries = [[2,1,0,1]]

// Output: [5]

 

// Constraints:

// 1 <= nums[i] <= 10^9
// 1 <= nums.length <= 10^5
// 1 <= k <= 5
// 1 <= queries.length <= 2 * 10^4
// queries[i] == [indexi, valuei, starti, xi]
// 0 <= indexi <= nums.length - 1
// 1 <= valuei <= 10^9
// 0 <= starti <= nums.length - 1
// 0 <= xi <= k - 1


// Solution:



class Solution {
public:
    int n,k;
    vector<int> p,a;
    vector<array<int,25>> c;
    void mg(int nd){
        int l=2*nd,r=2*nd+1;
        p[nd]=p[l]*p[r]%k;
        for(int i=0;i<k;i++){
            int t=i*p[l]%k;
            for(int j=0;j<k;j++) c[nd][i*k+j]=c[l][i*k+j]+c[r][t*k+j];
        }
    }
    void leaf(int nd,int v){
        for(int i=0;i<k*k;i++) c[nd][i]=0;
        p[nd]=v%k;
        for(int i=0;i<k;i++) c[nd][i*k+i*p[nd]%k]=1;
    }
    void bld(int nd,int l,int r){
        if(l==r){ leaf(nd,a[l]); return; }
        int m=(l+r)/2;
        bld(2*nd,l,m); bld(2*nd+1,m+1,r);
        mg(nd);
    }
    void upd(int nd,int l,int r,int i,int v){
        if(l==r){ leaf(nd,v); return; }
        int m=(l+r)/2;
        if(i<=m) upd(2*nd,l,m,i,v); else upd(2*nd+1,m+1,r,i,v);
        mg(nd);
    }
    void qry(int nd,int l,int r,int ql,int &st,vector<int>& res){
        if(r<ql) return;
        if(l>=ql){
            for(int j=0;j<k;j++) res[j]+=c[nd][st*k+j];
            st=st*p[nd]%k;
            return;
        }
        int m=(l+r)/2;
        qry(2*nd,l,m,ql,st,res);
        qry(2*nd+1,m+1,r,ql,st,res);
    }
    vector<int> resultArray(vector<int>& nums, int kk, vector<vector<int>>& queries) {
        n=nums.size(); k=kk; a=nums;
        p.assign(4*n,0); c.assign(4*n,{});
        bld(1,0,n-1);
        vector<int> ans;
        for(int i=0;i<queries.size();i++){
            int id=queries[i][0],v=queries[i][1],s=queries[i][2],x=queries[i][3];
            upd(1,0,n-1,id,v);
            int st=1%k;
            vector<int> res(k,0);
            qry(1,0,n-1,s,st,res);
            ans.push_back(res[x]);
        }
        return ans;
    }
};