class Solution {
    private int ans;

    public int tilingRectangle(int n, int m) {
        if (n > m) {
            int temp = n;
            n = m;
            m = temp;
        }

        ans = n * m;
        int[] height = new int[m];
        dfs(height, n, m, 0);
        return ans;
    }

    private void dfs(int[] height, int n, int m, int used) {
        if (used >= ans) return;

        int minHeight = Integer.MAX_VALUE;
        int pos = -1;

        // Find leftmost minimum height
        for (int i = 0; i < m; i++) {
            if (height[i] < minHeight) {
                minHeight = height[i];
                pos = i;
            }
        }

        // Completely filled
        if (minHeight == n) {
            ans = used;
            return;
        }

        // Find maximum width with same height
        int end = pos;
        while (end < m && height[end] == minHeight)
            end++;

        int maxSize = Math.min(end - pos, n - minHeight);

        // Try larger squares first
        for (int size = maxSize; size >= 1; size--) {

            for (int j = pos; j < pos + size; j++)
                height[j] += size;

            dfs(height, n, m, used + 1);

            for (int j = pos; j < pos + size; j++)
                height[j] -= size;
        }
    }
}