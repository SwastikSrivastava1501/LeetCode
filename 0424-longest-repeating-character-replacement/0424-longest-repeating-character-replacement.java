class Solution {
    public int characterReplacement(String s, int k) {

        int left = 0, right = 0, maxFreq = 0, ans = 0;
        int[] arr = new int[26];
        while(right < s.length()) {
            arr[s.charAt(right) - 'A']++;
            maxFreq = Math.max(maxFreq, arr[s.charAt(right) - 'A']);
            if((right - left + 1 - maxFreq) > k) {
                arr[s.charAt(left) - 'A']--;
                left++;
            }
            if((right - left + 1 - maxFreq) <= k)ans = Math.max(ans, right - left + 1);
            right++;
        }
        return ans;
    }
}