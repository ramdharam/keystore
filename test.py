def longestPalindrome(s):
    """
    :type s: str
    :rtype: str
    """
    if len(s) == 0:
        return ''
    if len(s) == 1:
        return s
    n = len(s)
    sol = [[None for _ in xrange(n)] for _ in xrange(n)]
    ## len 1
    for i in xrange(n):
        sol[i][i] = True
        start, end = i, i
    ## for len 2
    for i in xrange(n - 1):
        if s[i] == s[i + 1]:
            sol[i][i + 1] = True
            start, end = i, i + 1
    ## for len >=3
    for i in xrange(3, n+1):
        for j in xrange(n - i +1):
            k = j + i - 1
            if s[j] == s[k] and sol[j + 1][k - 1] == True:
                sol[j][k] = True
                start, end = j, k
    return s[start:end + 1]


out = longestPalindrome("abcba")
print out