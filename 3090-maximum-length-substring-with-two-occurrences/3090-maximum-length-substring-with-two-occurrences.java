class Solution {
    public int maximumLengthSubstring(String s) {

        int[] count = new int[26];
        int max = 0;
        int left = 0;

        for (int right = 0; right < s.length(); right++) {
            
            int charIdx = s.charAt(right) - 'a';
            count[charIdx]++;

            while (count[charIdx] > 2) {
                count[s.charAt(left) - 'a']--;
                left++;
            }

            max = Math.max(max, right - left + 1);
        }

        return max;
    }
}