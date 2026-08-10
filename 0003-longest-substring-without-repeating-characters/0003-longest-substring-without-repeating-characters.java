import java.util.HashSet;
import java.util.Set;

class Solution {
    public int lengthOfLongestSubstring(String s) {
        int n = s.length();
        int res = 0;
        int left = 0;
        Set<Character> charSet = new HashSet<>();
        
        for (int right = 0; right < n; right++) {
            while (charSet.contains(s.charAt(right))) {
                charSet.remove(s.charAt(left));
                left++;
            }
            charSet.add(s.charAt(right));
            res = Math.max(res, right - left + 1);
        }
        return res;
    }
}