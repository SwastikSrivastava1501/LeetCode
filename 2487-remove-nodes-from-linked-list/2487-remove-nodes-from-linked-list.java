class Solution {
    public ListNode removeNodes(ListNode head) {

        if (head == null || head.next == null) {
            return head;
        }

        Stack<ListNode> stack = new Stack<>();

        ListNode curr = head;

        while (curr != null) {

            // Remove nodes that have a greater value on their right
            while (!stack.isEmpty() && stack.peek().val < curr.val) {
                stack.pop();
            }

            stack.push(curr);
            curr = curr.next;
        }

        // Rebuild the linked list from the stack
        ListNode next = null;

        while (!stack.isEmpty()) {
            curr = stack.pop();
            curr.next = next;
            next = curr;
        }

        return next;
    }
}