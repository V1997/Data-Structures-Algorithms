import sys
import operator
from collections import deque
from collections import Counter
class Node(object):
    
    def __init__(self, freq = None, char = None):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    def set_value(self, freq, char):
        self.char = char
        self.freq = freq
    
    def get_char(self):
        return self.char

    def get_freq(self):
        return self.freq
         
    def set_left_child(self,left):
        self.left = left
    
    def set_right_child(self, right):
        self.right = right
    
    def get_left_child(self):
        return self.left
    
    def get_right_child(self):
        return self.right
    
    def has_left_child(self):
        return self.left != None
    
    def has_right_child(self):
        return self.right != None
    

class Stack:
    
    def __init__(self, initial_size = 100):
        self.arr = [0 for _ in range(initial_size)]
        self.next_index = 0
        self.num_elements = 0
    
    def push(self, data):
        if self.next_index == len(self.arr):
            print("Out of space! Increasing array capacity ...")
            self._handle_stack_capacity_full()
        
        self.arr[self.next_index] = data
        self.next_index += 1
        self.num_elements += 1
    def top(self):
        return self.arr[self.num_elements-1] 
    def pop(self):
        if self.is_empty():
            self.next_index = 0
            return None
        self.next_index -= 1
        self.num_elements -= 1
        return self.arr[self.next_index]
    
    def size(self):
        return self.num_elements
    
    def is_empty(self):
        return self.num_elements == 0
    
    def _handle_stack_capacity_full(self):
        old_arr = self.arr
        
        self.arr = [0 for _ in range( 2* len(old_arr))]
        for index, element in enumerate(old_arr):
            self.arr[index] = element
    def __repr__(self):
        if not self.is_empty():
            s = "<bottom here>\n_________________\n"
            for item in self.arr:
                if type(item).__name__ == 'Tree':
                    s += "\n_________________\n" + 'root: ' + str(item.get_root().get_freq()) + "\n"
                else:
                    s += "\n_________________\n" + item.get_char() + str(item.get_freq()) + "\n"
                s += "\n_________________\n<top here>"
                return s
        else:
            return "<Stack is empty>"


class Queue():
    def __init__(self):
        self.q = deque()
    
    def enq(self,value):
        self.q.appendleft(value)
    
    def deq(self):
        if len(self.q) > 0:
            return self.q.pop()
        else:
            return None
    
    def __len__(self):
        return len(self.q)
    
    def __repr__(self):
        if len(self.q) > 0:
            s = "<enqueue here>\n_________________\n"
            for item in self.q:
                if type(item).__name__ == 'Tree':
                    s += "\n_________________\n" + 'root: ' + str(item.get_root().get_freq()) + "\n"
                else:
                    s += "\n_________________\n" + item.get_char() + str(item.get_freq()) + "\n"
            s += "\n_________________\n<dequeue here>"
            return s
        else:
            return "<queue is empty>"
def _node_specific_has_left_child(node):
    if type(node).__name__ == 'Node':
        return node.has_left_child()
    elif type(node).__name__ == 'Tree':
        return node.get_root().has_left_child()
        
def _node_specific_has_right_child(node):
    if type(node).__name__ == 'Node':
        return node.has_right_child()
    elif type(node).__name__ == 'Tree':
        return node.get_root().has_right_child()
def _node_specific_get_left_child(node):
    if type(node).__name__ == 'Node':
        return node.get_left_child()
    elif type(node).__name__ == 'Tree':
        return node.get_root().get_left_child()

def _node_specific_get_right_child(node):
    if type(node).__name__ == 'Node':
        return node.get_right_child()
    elif type(node).__name__ == 'Tree':
        return node.get_root().get_right_child()
def compare_by_char(node, new_node):
    if _node_specific_char(new_node) == _node_specific_char(node):
        return 0
    else:
        return -1
 
class Tree():
    def __init__(self):
        self.root = None
    
    def set_root(self,freq, char=None):
        self.root = Node(freq, char=None)
    
    def get_root(self):
        return self.root
   
    def compare(self,node, new_node):
        """
            0 means new_node equals node
            -1 means new node less than existing node
            1 means new node greater than existing node
            """
        if _node_specific_freq(new_node) == _node_specific_freq(node):
#compare chars as well
            #return compare_by_char(node, new_node) 
            return 0
        elif _node_specific_freq(new_node) < _node_specific_freq(node):
            return -1
        else:
            return 1
    
    def insert(self,new_node):
        #new_node = Node(new_value)
        node = self.get_root()
        if node == None:
            self.root = new_node
            return
        
        while(True):
            comparison = self.compare(node, new_node)
            if comparison == 0:
                # override with new node
                node = new_node
                break # override node, and stop looping
            elif comparison == -1:
                # go left
                if node.has_left_child():
                    node = node.get_left_child()
                else:
                    node.set_left_child(new_node)
                    break #inserted node, so stop looping
            else: #comparison == 1
                # go right
                if node.has_right_child():
                    node = node.get_right_child()
                else:
                    node.set_right_child(new_node)
                    break # inserted node, so stop looping
    
    
    def search(self,char,freq):
        node = self.get_root()
        s_node = Node(freq, char)
        while(True):
            comparison = self.compare(node,s_node)
            if comparison == 0:
                return True
            elif comparison == -1:
                if _node_specific_has_left_child(node): 
                    node = _node_specific_get_left_child(node)
                else:
                    return False
            else:
                if _node_specific_has_right_child(node):#.has_right_child():
                    node = _node_specific_get_right_child(node)#.get_right_child()
                else:
                    return False
    def __repr__(self):
        level = 0
        q = Queue()
        visit_order = list()
        node = self.get_root()
        q.enq( (node,level) )
        while(len(q) > 0):
            node, level = q.deq()
            if node == None:
                visit_order.append( ("<empty>", level))
                continue
            visit_order.append( (node, level) )
            if node.has_left_child():
                q.enq( (node.get_left_child(), level +1 ))
            else:
                q.enq( (None, level +1) )
            
            if node.has_right_child():
                q.enq( (node.get_right_child(), level +1 ))
            else:
                q.enq( (None, level +1) )
    
        s = "Tree\n"
        previous_level = -1
        for i in range(len(visit_order)):
            node, level = visit_order[i]
            if level == previous_level:
                s += " | " + str(node)
            else:
                s += "\n" + str(node)
                previous_level = level


        return s

class State(object):
    def __init__(self,node):
        self.node = node
        self.visited_left = False
        self.visited_right = False
    
    def get_node(self):
        return self.node
    
    def get_visited_left(self):
        return self.visited_left
    
    def get_visited_right(self):
        return self.visited_right
    
    def set_visited_left(self):
        self.visited_left = True
    
    def set_visited_right(self):
        self.visited_right = True
def convert(list): 
       
# Converting integer list to string list 
# and joining the list using join() 
    res = str("".join(map(str, list))) 
                             
    return res 
                              
def pre_order_with_stack(tree, debug_mode=False):
    visit_order = list()
    stack = Stack()
    stack_of_codes = Stack()
    node = tree.get_root()
    #visit_order.append(node.get_value())
    visit_order.append(str(_node_specific_char(node)) + ':' +str(_node_specific_freq(node)))
    state = State(node)
    stack.push(state)
    codes = {} 
    while(node):
        if _node_specific_has_left_child(node) and not state.get_visited_left():
            state.set_visited_left()
            node = _node_specific_get_left_child(node)
            visit_order.append(str(_node_specific_char(node)) + ':' +str(_node_specific_freq(node)))
            state = State(node)
            stack.push(state)
            stack_of_codes.push(0)
        
        elif _node_specific_has_right_child(node) and not state.get_visited_right():
            state.set_visited_right()
            node = _node_specific_get_right_child(node)
            #visit_order.append(_node_specific_char(node))
            visit_order.append(str(_node_specific_char(node)) + ':' +str(_node_specific_freq(node)))
            state = State(node)
            stack.push(state)
            stack_of_codes.push(1)
        
        else:
            #make tempory copy
            tmp = []
            while not stack_of_codes.is_empty():
                tmp.append(stack_of_codes.pop())
            codes[_node_specific_char(node)] = convert(list(reversed(tmp)))
            for i in range(len(tmp)-1, 0, -1):
                stack_of_codes.push(tmp[i])
#do normal stuff for traversing
            stack.pop()
            if not stack.is_empty():
                state = stack.top()
                node = state.get_node()
            else:
                node = None

    return visit_order, codes

def _node_specific_freq(node):
    if type(node).__name__ == 'Tree':
        return node.get_root().get_freq()
    elif type(node).__name__ == 'Node':
        return node.get_freq()
def _node_specific_char(node):
    if type(node).__name__ == 'Tree':
        return node.get_root().get_char()
    elif type(node).__name__ == 'Node':
        return node.get_char()
def encode_data(data, tree):
    '''
    tree: str to encode, uffman built tree
    return: encoded data, and tree
    '''
    data = data.lower().replace(' ', '|')
    data_freq = Counter(data.lower().replace(' ', '|'))
    visit_order, codes = pre_order_with_stack(tree)
    print(visit_order)
    for c in codes.keys():
        print(c, codes[c])

    return tree, [codes[i] for i in data]
def huffman_encoding(data):
    #lower case
    data = data.lower()
#empty data
    if len(data) == 0 :
        return -1,-1,-1

    if len(set(data)) == 1:
        return '1'*len(data), [1]*len(data), data[0]
    #replace white space by `|` separator
    data = data.replace(' ', '|')
    #frequency of characters
    freq = {}
    for char in list(data):
        if char in freq.keys():
            freq[char] += 1
        else:
            freq[char] = 1 
    #sort in descending order
    #sorted_freq = sorted(freq.items(), key=operator.itemgetter(1), reverse=True)
#sorted by value then key
    sorted_freq = sorted(freq.items(), key=lambda x: (x[1],x[0]), reverse=True)
    #build a tree
    s = Stack()
    for tpl in sorted_freq:
        node = Node(tpl[-1], tpl[0])
        s.push(node)
    for item in s.arr:
        if type(item).__name__ == 'Node':
            print(item.get_char(), item.get_freq())
    while s.num_elements > 1:
        a = s.pop() 
        b = s.pop()
        #create a tree
        t = Tree()
        t.set_root(_node_specific_freq(a) + _node_specific_freq(b)) 
        #print('root: ', a.get_freq() + b.get_freq(), t.get_root().get_freq())
        if _node_specific_freq(a) < t.get_root().get_freq():
            t.get_root().set_left_child(a)
            t.get_root().set_right_child(b)
        else:
            t.get_root().set_left_child(a)
            t.get_root().set_right_child(b)
        #add to stack
        top = s.top()
        #node
        #if type(top).__name__ == 'Node':
        if _node_specific_freq(top) != None and _node_specific_freq(top) >= t.get_root().get_freq():
            s.push(t)
            #print('pushing on top')
        else:#pop lighter nodes
            tmp_stack = []
            while _node_specific_freq(top) != None and  _node_specific_freq(top) < t.get_root().get_freq():
                tmp_stack.append(s.pop())
                top = s.top()
                #print('val: ', _node_specific_freq(top), t.get_root().get_freq())
                if _node_specific_freq(top) == None:
                    break
            s.push(t)
            #print('size of lighter nodes: ', len(tmp_stack))
            for tt in list(reversed(tmp_stack)): 
                s.push(tt)
        #break
    #encode_data(data, s.top())
    #get codes for each character
    visit_order, codes = pre_order_with_stack(s.top())#s.top() is the tree
    '''print(visit_order)
    for c in codes.keys():
        print(c, codes[c])'''

    #return convert([codes[i] for i in data]), s.top()
    return convert([codes[i] for i in data]), [codes[i] for i in data], s.top()

def huffman_decoding(encoded_data, tree):
    decoded_data = []
    if encoded_data == -1: #empty string
        return
    if sum([int(i) for i in encoded_data]) == len(encoded_data):#repeating elements such as AAAAAAAA
        return tree*len(encoded_data)
    for code in encoded_data:
        node = tree.get_root()
        while node:
            for c in code:
                if c == '0':
                    node =  _node_specific_get_left_child(node) 
                elif c == '1':
                    node = _node_specific_get_right_child(node)
                else:
                   print('ERROR')
                   sys.exit(0) 
                if  _node_specific_char(node) != None:
                    decoded_data.append(_node_specific_char(node))
    return ''.join(decoded_data).replace('|', ' ')
if __name__ == "__main__":
    print('------------------TEST-1--------------------')
    a_great_sentence = "The bird is the word"

    print ("The size of the data is: {}\n".format(sys.getsizeof(a_great_sentence)))
    print ("The content of the data is: {}\n".format(a_great_sentence))
    
    #huffman_encoding(a_great_sentence)
    encoded_data, encoded_data_lst, tree = huffman_encoding(a_great_sentence)
    print('en: ', encoded_data)
    
    print ("The size of the encoded data is: {}\n".format(sys.getsizeof(int(encoded_data, base=2))))
    print ("The content of the encoded data is: {}\n".format(encoded_data))
     
    decoded_data = huffman_decoding(encoded_data_lst, tree)
    print ("The size of the decoded data is: {}\n".format(sys.getsizeof(decoded_data)))
    print ("The content of the encoded data is: {}\n".format(decoded_data))

    print('------------------TEST-2--------------------')
    a = "Hufman coding is a data compression algorithm."
    encoded_data, encoded_data_lst, tree = huffman_encoding(a)
    print(encoded_data)
    print(huffman_decoding(encoded_data_lst, tree))

    print('------------------TEST-3--------------------')#empty string
    encoded_data, encoded_data_lst, tree = huffman_encoding("")
    print(encoded_data)#prints -1
    print(huffman_decoding(encoded_data_lst, tree)) #prints None

    print('------------------TEST-4--------------------')
    encoded_data, encoded_data_lst, tree = huffman_encoding("AAAAAAAAA")
    print(encoded_data)#prints 111111111
    print(encoded_data_lst)
    print(huffman_decoding(encoded_data_lst, tree)) #prints None