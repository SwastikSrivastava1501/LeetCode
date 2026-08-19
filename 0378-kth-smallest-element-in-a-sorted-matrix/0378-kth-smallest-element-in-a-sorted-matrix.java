class Solution {
    public int kthSmallest(int[][] matrix, int k) {

        int n = matrix.length;
        int low = matrix[0][0], high = matrix[n - 1][n - 1], ans = -1;
        while(low <= high){
            int mid = low + (high - low)/2;
            if(check(matrix, mid, k)){
                ans = mid;
                high = mid - 1;
            } else{
                low = mid + 1;
            }
        } 
        return ans;       
    }

    private boolean check(int[][]matrix, int element, int k){
        int count = 0;
        int i = matrix.length - 1, j = 0;
        while(i >= 0 && j < matrix[0].length){
            if(matrix[i][j] <= element){
                count += (i + 1);
                j++;
            } else{
                i--;
            }
        }
        return count >= k;
    }
}