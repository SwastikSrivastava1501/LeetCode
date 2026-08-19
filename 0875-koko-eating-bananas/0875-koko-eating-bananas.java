class Solution {

    public boolean canFinish(int[] piles, int h, int k) {
        long hours = 0;

        for (int bananas : piles) {
            hours += (bananas + k - 1) / k;

            if (hours > h) {
                return false;
            }
        }

        return true;
    }

    public int minEatingSpeed(int[] piles, int h) {
        int low = 1;
        int high = 0;

        for (int bananas : piles) {
            high = Math.max(high, bananas);
        }

        while (low < high) {
            int mid = low + (high - low) / 2;

            if (canFinish(piles, h, mid)) {
                high = mid;
            } else {
                low = mid + 1;
            }
        }

        return low;
    }
}