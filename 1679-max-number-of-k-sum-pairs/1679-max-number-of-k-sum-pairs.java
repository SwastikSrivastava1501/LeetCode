class Solution {
    public int maxOperations(int[] nums, int k) {
        
        int n = nums.length;
        Arrays.sort(nums);

        int low = 0, high = n - 1, count = 0;

        while(low < high) {
            int sum = nums[low] + nums[high];
            if(sum == k) {
                low++;
                high--;
                count++;
            } else if(sum > k) {
                high--;
            } else {
                low++;
            }
        }
        return count;
    }
}