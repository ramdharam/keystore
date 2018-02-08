def lengthOfLongestSubstring(s):
    """
    :type s: str
    :rtype: int
    """
    if len(s) == 0:
        return 0
    mydict = {}
    i = 0
    n = len(s)
    start = 0
    maxLen = 0
    while i < n:
        if s[i] not in mydict.keys():
            mydict[s[i]] = i
        elif s[i] in mydict.keys() and mydict[s[i]] < start:
            mydict[s[i]] = i
        else:
            start = mydict[s[i]] + 1
            mydict[s[i]] = i
        maxLen = max(maxLen, i - start + 1)
        i += 1
    return maxLen


print (lengthOfLongestSubstring("abba"))