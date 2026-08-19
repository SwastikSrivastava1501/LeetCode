class Solution {
    public int hIndex(int[] citations) {
        int n = citations.length;
        int low = 0, high = n - 1;
        int k = 0;

        while(low <= high){
            int mid = low + (high - low)/2;
            if(n - mid <= citations[mid]){
                k = n - mid;
                high = mid - 1;
            } else{
                low = mid + 1;
            }
        }
        return k;
    }
}