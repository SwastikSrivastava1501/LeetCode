class Solution {
    public int shipWithinDays(int[] weights, int days) {

        int maxWeight = -1, totalWeight = 0;
        for(int weight : weights){
            maxWeight = Math.max(maxWeight, weight);
            totalWeight += weight;
        }

        int low = maxWeight , high = totalWeight;
        while(low < high){
            int mid = (high + low)/2;
            int daysNeeded = 1, currWeight = 0;
            for(int weight : weights){
                if(currWeight + weight > mid){
                    daysNeeded++;
                    currWeight = 0;
                }
                currWeight += weight;
            }
            if(daysNeeded > days){
                low = mid + 1;
            } else{
                high = mid;
            }
        }
        return low;
    }
}