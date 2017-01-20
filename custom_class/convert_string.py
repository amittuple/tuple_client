class convert_string:

    def __init__(self):
        pass

    def convert_Str(self,input_self):
        if input_self is None:
            print "input_self is none"
            return None

        Str_Int=" "
        for x in input_self:
            if isinstance(x,str):
                Str_Int = Str_Int + x
            elif isinstance(x, int):
                Str_Int = Str_Int + x
            elif isinstance(x, float):
                Str_Int = Str_Int + x
        return Str_Int

    def convert_gt_lt_Standrd(self,input_gt_lt):
        if input_gt_lt is None:
            print 'input_gt_lt is none'
            return None

        list_gt_lt=[]
        for x in input_gt_lt:
            if x=='gt' or x=='gt;':
                list_gt_lt.append('>')
            elif x=='lt' or x=='lt;':
                list_gt_lt.append('<')
            elif x=='eq' or x=='eq;':
                list_gt_lt.append('=')
            else:
                list_gt_lt.append(x)
        return list_gt_lt

    def remove_extra_space_fromInput(self,space_input):
        if space_input is None:
            print 'remove extra space is None'
            return None

        list_0 = []
        for x in space_input:
            if x == "":
                print "found space"
            else:
                list_0.append(x)
        return list_0