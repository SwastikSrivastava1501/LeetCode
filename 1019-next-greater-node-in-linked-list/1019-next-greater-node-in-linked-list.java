/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode() {}
 *     ListNode(int val) { this.val = val; }
 *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }
 * }
 */
class Solution {
    public int[] nextLargerNodes(ListNode head) {
        List<Integer> list = new ArrayList<>();

        while(head != null) {
            list.add(head.val);
            head = head.next;
        }

        Stack<Integer> stack = new Stack<>();
        int[] ans = new int[list.size()];

        for(int i = 0; i < list.size(); i++) {
            
            while(!stack.isEmpty() && list.get(i) > list.get(stack.peek())) ans[stack.pop()] = list.get(i);

            stack.push(i);
        }
        return ans;
    }
}