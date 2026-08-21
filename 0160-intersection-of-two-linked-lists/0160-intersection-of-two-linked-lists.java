/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode(int x) {
 *         val = x;
 *         next = null;
 *     }
 * }
 */
public class Solution {
    public ListNode getIntersectionNode(ListNode headA, ListNode headB) {
        
        if (headA == null || headB == null) {
            return null;
        }

        ListNode tmp1 = headA;
        ListNode tmp2 = headB;

        while (tmp1 != tmp2) {
            
            if (tmp1 == null) {
                tmp1 = headB;
            } else {
                tmp1 = tmp1.next;
            }

            if (tmp2 == null) {
                tmp2 = headA;
            } else {
                tmp2 = tmp2.next;
            }
        }

        return tmp1;
    }
}