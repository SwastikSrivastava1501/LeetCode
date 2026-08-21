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
    public ListNode removeNthFromEnd(ListNode head, int n) {

        ListNode DummyNode = new ListNode(0);
        DummyNode.next = head;
        ListNode Slow = DummyNode;
        ListNode Fast = DummyNode;

        for(int i = 0; i<=n; ++i) 
        {

            Fast = Fast.next;
        }

        while(Fast != null) {
            Fast = Fast.next;
            Slow = Slow.next;
        }

        Slow.next = Slow.next.next;

        return DummyNode.next;
    }
}