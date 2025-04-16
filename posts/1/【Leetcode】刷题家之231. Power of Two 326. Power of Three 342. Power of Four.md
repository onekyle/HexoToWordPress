---
title: 231. Power of Two 326. Power of Three 342. Power of Four
layour: post
uuid: fasw2d-arr-ppp-fasfw-wqr2fg
tags: [LeetCode]
categories: LeetCode
index_img: https://img.164314.xyz/2025/02/11da67747e9a7fbbf40ddc5a151491b3.png
date: 2025-02-21 18:07:08
---
# 请看题

![](https://img.164314.xyz/2025/02/11da67747e9a7fbbf40ddc5a151491b3.png)

![](https://img.164314.xyz/2025/02/a47e17b2e4f5b5fcb0b9e22a636befdc.png)

![](https://img.164314.xyz/2025/02/057254b1685a1047f45e2f37ba3764f5.png)

题目很简单，判断一个传进来的数是否是2 or 3 or 4的幕。

对于这个，有写一个对数的函数的解法也有另外的解法，那么这里我用一个递归的方法。 

首先是判断是否为2 的幕。只需要几个if，比如传入的数为负数那么直接可以确认这一定就不是，另外如果取模的结果不是等于0那么肯定也不是，最后再写一个递归结束的条件，也就是传入的数是否为1，这个返回true。在进行递归调用的时候需要传入当前数的一半。

## 看答案
```
bool isPowerOfTwo(int n) {
        if(n <= 0 || n % 2 != 0 && n != 1){
            return false;
        }
        if(n == 1){
            return true;
        }
        return isPowerOfTwo(n / 2);
    }

```

另外两题也是一样的解法，只不过是把2换成了3 或 4

```
bool isPowerOfThree(int n) {
        if(n <= 0){
            return false;
        }
        if(n == 1){
            return true;
        }
        if(n % 3 != 0){
            return false;
        }
        return isPowerOfThree(n / 3);
    }
```

```
bool isPowerOfFour(int n) {
        if(n <= 0){ return false; }
        if( n == 1){
            return true;
        }
        if(n % 4 != 0){ return false;}
        return isPowerOfFour(n / 4);
    }
```
