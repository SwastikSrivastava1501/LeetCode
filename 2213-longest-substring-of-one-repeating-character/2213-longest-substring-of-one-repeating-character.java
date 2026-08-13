class Solution {

    class Node {
        char leftChar, rightChar;
        int leftLen, rightLen, maxLen, len;

        Node(char c) {
            leftChar = rightChar = c;
            leftLen = rightLen = maxLen = len = 1;
        }

        Node() {}
    }

    Node[] tree;

    public int[] longestRepeating(
            String s,
            String queryCharacters,
            int[] queryIndices) {

        int n = s.length();
        int k = queryIndices.length;

        tree = new Node[4 * n];

        build(s, 1, 0, n - 1);

        int[] ans = new int[k];

        for (int i = 0; i < k; i++) {
            int index = queryIndices[i];
            char ch = queryCharacters.charAt(i);

            update(1, 0, n - 1, index, ch);

            ans[i] = tree[1].maxLen;
        }

        return ans;
    }

    private void build(String s, int node, int l, int r) {

        if (l == r) {
            tree[node] = new Node(s.charAt(l));
            return;
        }

        int mid = l + (r - l) / 2;

        build(s, node * 2, l, mid);
        build(s, node * 2 + 1, mid + 1, r);

        tree[node] = merge(tree[node * 2], tree[node * 2 + 1]);
    }

    private void update(
            int node,
            int l,
            int r,
            int index,
            char ch) {

        if (l == r) {
            tree[node] = new Node(ch);
            return;
        }

        int mid = l + (r - l) / 2;

        if (index <= mid) {
            update(node * 2, l, mid, index, ch);
        } else {
            update(node * 2 + 1, mid + 1, r, index, ch);
        }

        tree[node] = merge(tree[node * 2], tree[node * 2 + 1]);
    }

    private Node merge(Node left, Node right) {

        Node res = new Node();

        res.len = left.len + right.len;

        res.leftChar = left.leftChar;
        res.rightChar = right.rightChar;

        // Prefix
        res.leftLen = left.leftLen;

        if (left.leftLen == left.len &&
            left.rightChar == right.leftChar) {

            res.leftLen = left.len + right.leftLen;
        }

        // Suffix
        res.rightLen = right.rightLen;

        if (right.rightLen == right.len &&
            left.rightChar == right.leftChar) {

            res.rightLen = right.len + left.rightLen;
        }

        // Maximum inside either segment
        res.maxLen = Math.max(left.maxLen, right.maxLen);

        // Combine suffix of left + prefix of right
        if (left.rightChar == right.leftChar) {
            res.maxLen = Math.max(
                res.maxLen,
                left.rightLen + right.leftLen
            );
        }

        return res;
    }
}