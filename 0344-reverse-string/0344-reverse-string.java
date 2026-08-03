class Solution {
    public void reverseString(char[] s) {

        char[] temp = new char[s.length];
        for(int i = s.length - 1, j = 0; i>= 0; i--, j++){
            temp[j] = s[i];
        }
        for (int i = 0; i < s.length; i++){
            s[i] = temp[i];           
        }
        
    }
}