class Solution {
    public int stoneGameV(int[] stoneValue) {
        int[][] dp = new int[stoneValue.length][stoneValue.length];
        for(int[] d : dp){
            Arrays.fill(d,-1);
        }

        int[] prefix = new int[stoneValue.length+1];
        for(int i = 0; i < stoneValue.length; i++){
            prefix[i+1] = prefix[i] + stoneValue[i];
        }

        return solve(0, stoneValue.length-1, stoneValue, dp, prefix);
    }

    public int solve(int i, int j, int[] stoneValue, int[][] dp, int[] prefix){
        if(i == j) return 0;

        if(dp[i][j] != -1) return dp[i][j];

        int ans = 0;

        for(int k = i; k < j; k++){
            int leftSum = prefix[k+1] - prefix[i];
            int rightSum = prefix[j+1] - prefix[k+1];

            if(leftSum < rightSum){
                ans = Math.max(ans, leftSum + solve(i, k, stoneValue, dp, prefix));
            }
            else if(rightSum < leftSum){
                ans = Math.max(ans, rightSum + solve(k+1, j, stoneValue, dp, prefix));
            }
            else{
                ans = Math.max(ans,
                    Math.max(
                        leftSum + solve(i, k, stoneValue, dp, prefix),
                        rightSum + solve(k+1, j, stoneValue, dp, prefix)
                    )
                );
            }
        }

        return dp[i][j] = ans;
    }
}