class Parentheses():
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.integrity = self.check_integrity
        self.size = len(left)

    def check_integrity(self):
        if len(self.left) < len(self.right):
            print('missing {} left parentheses'.format(len(self.right) - len(self.left)))
            return 0
        elif len(self.left) > len(self.right):
            print('missing {} right parentheses'.format(len(self.left) - len(self.right)))
            return 0
        return 1


class MyTest():

    def test(self, context):
        p = self.get_parentheses(context)
        t = self.get_context(context, p)
        print(t)

    def get_parentheses(self, context):
        left = []
        right = []
        chars = [char for char in context]
        for idx, char in enumerate(chars):
            if char == '(':
                left.append(idx)
            elif char == ')':
                right.append(idx)
        right.sort(reverse=True)
        p = Parentheses(left, right)
        return p

    def get_context(self, context, p):
        if p.size == 1:
            return self.interpret(context)
        else:
            index = p.size - 1
            left = p.left[index]
            right = p.right[index]
            while left > right:
                index =index-1
                right = p.right[index]
            char = context[left- 1:left]
            offset = self.offset(char)
            start = left - offset
            end = right + 1
            context_seg = context[start:end]
            s1 = context[0:start]
            s3 = context[end:len(context)]
            new_end = len(context)
            context = context[0:start] + self.interpret(context_seg) + context[end:len(context)]
            p = self.get_parentheses(context)
            return self.get_context(context, p)

    # ADD
    # MULT
    # RANK
    # TSUPPLY

    def offset(self, char):
        if char == 'D':
            return 3
        elif char == 'Y':
            return 7
        else:
            return 4

    def interpret(self, context):
        context = context.replace(')', '')
        if context[0:1] == 'A':
            context = context.replace('ADD(', '')
            arr = context.split(',')
            for i in range(0, 1):
                if len(arr[i]) >= 3:
                    arr[i] = arr[i].split('=')[1]
            return str(self.add(int(arr[0]), int(arr[1])))
        elif context[0:1] == 'M':
            x = 1
        elif context[0:1] == 'R':
            x = 1
        else:
            x = 1

        return 1

    def add(self, a, b):
        return a + b

    def mult(self, a, b):
        return a * b


if __name__ == "__main__":
    # MyTest().test("ADD(ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,4))))))),ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,4)))))))))))),ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,4))))))")
    #MyTest().test("ADD(ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,4))))))),ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,4)))))))))))),ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,4))))))")
    MyTest().test("ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,ADD(x=5,4))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))")