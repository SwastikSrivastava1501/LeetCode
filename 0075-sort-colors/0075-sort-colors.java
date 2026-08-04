class Solution {
    public void sortColors(int[] nums) {
        
        int countA = 0;
        int countB = 0;
        int countC = 0;

       for(int num : nums) {

        if(num == 0){
        countA++;
        } else if(num == 1) {
        countB++;
        } else {
        countC++;
        }
       } 

       int index = 0;
       for(int i = 0; i < countA; i++) {
        nums[index++] = 0;
       }
       for(int i = 0; i < countB; i++) {
        nums[index++] = 1;
       }
       for(int i = 0; i < countC; i++) {
        nums[index++] = 2;
       }
    }
}