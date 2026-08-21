/**
 * Definition for singly-linked list.
 * public class ListNode {
 * int val;
 * ListNode next;
 * ListNode() {}
 * ListNode(int val) { this.val = val; }
 * ListNode(int val, ListNode next) { this.val = val; this.next = next; }
 * }
 */
class Solution {
    public ListNode removeNodes(ListNode head) {
        
        if (head == null || head.next == null) {
            return head;
        }

        ListNode prev = head;   
        ListNode curr = head.next;

        while (curr != null) {
            ListNode next = curr.next;
            curr.next = prev;
            prev = curr;
            curr = next;
        }

        head.next = null;
        head = prev;     
        
        prev = head;
        curr = head.next;

        while (curr != null) {
            if (curr.val < prev.val) {
                
                curr = curr.next;
            } else {
              
                ListNode next = curr.next;
                curr.next = prev;
                prev = curr;
                curr = next;
            }
        }

        head.next = null; 
        return prev;      
    }
}