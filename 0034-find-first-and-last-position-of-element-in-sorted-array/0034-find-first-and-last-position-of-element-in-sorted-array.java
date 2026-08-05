class Solution {
    public int[] searchRange(int[] nums, int target) {

        int first = findPosition(nums, target, true);
        int last = findPosition(nums, target, false);

        return new int[] {first, last};        
    }

    private int findPosition(int[] nums, int target, boolean findFirst) {
         int low = 0;
         int high = nums.length - 1;
         int pos = -1;

         while(low <= high) {
            int mid = low + (high - low)/2;

            if(nums[mid] == target) {
                pos = mid;
                if(findFirst)
                high = mid - 1;
                else
                low = mid + 1;
            }
            else if(nums[mid] < target)
            low = mid + 1;
            else
            high = mid - 1;
         }
         return pos;
    }
}