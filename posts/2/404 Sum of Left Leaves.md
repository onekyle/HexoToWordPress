---
title: 404 Sum of Left Leaves
layour: post
uuid: fasw2d-arr-11ed-fasfw-wqr2gge
tags: [LeetCode]
categories: LeetCode
index_img: https://img.164314.xyz/img/2024/05/cd945897fbdd60bdfb0358b90f9a0d66.png
date: 2024-05-25 18:07:08
---


![](https://img.164314.xyz/img/2024/05/cd945897fbdd60bdfb0358b90f9a0d66.png)

# 请看题

![](https://img.164314.xyz/img/2024/05/5a728c2954d2f107f1f580021ea957bb.png)

# Example

![](https://img.164314.xyz/img/2024/05/95700cdb55801a86eb4c62c80b988b13.png)
![](https://img.164314.xyz/img/2024/05/b3cb4e5f86afb16e454881599258fb47.png)

# 解析

这一道题要求我们去计算左孩子的sum，怎么去计算呢？

想一想，判断左孩子要什么条件呢？

根据Example中我们可以看见，左孩子的下节点为空，那么根据if我们就可以写出如果当前节点不为空并且左孩子的左右节点为空那么就可以获取到值，然后计算

----

## Code

```
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    
    int sums(TreeNode *root)
    {
        int sum = 0;
        if(!root)
        {
            return 0;
        }
        if (root->left && !root->left->left && !root->left->right)  
        {
            sum += root->left->val;
        }
        sum += sumOfLeftLeaves(root->left) + sumOfLeftLeaves(root->right);
    
        return sum;  
    }

    int sumOfLeftLeaves(TreeNode* root) {
        if(!root)
        {
            return 0;
        }
        return sums(root);
        
    }
};
```


---
结束。
