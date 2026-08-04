class Solution {
    public int arrangeCoins(int n) {
        
        long low = 1, high = n;

        while(low <= high) {
            long mid = low + (high - low)/2;

            long CurrCoins = mid * (mid+1)/2;

            if(CurrCoins == n) {
                return (int)mid;
            }
            if(n < CurrCoins) {
                high = mid - 1;
            }
            else {
                low = mid + 1;
            }
        }
        return (int)high;
    }
}