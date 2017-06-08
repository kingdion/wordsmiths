# !/usr/bin/python
'''
Operational Transformation
Built by Dion Misic for Wordsmiths using Python 2.7

Given two operations from QuillJS give two transformed functions back.
Functions are split multipletimes for readability.

Contains two objects, OT_Char and OT_String for both
character-wise and string-wise operations, usage depends on the
specifications and design of the OT system. Any operational compression
can only be performed on string operations, therefore making OT_String the
ideal performant class. The two classes operate as control functions which
handle the transformations.

The conversion stage is specifically catered to work with QuillJS.


USAGE:
1. Initialise an OT object to a variable. (char or string)
OTC = OT_Char()

2. Pass in operations into transform function
new_ops = OTC.transform(op1, op2)


 *** EXAMPLE USAGE AT END OF DOC ***
'''

''' OT_Char Character-Wise Function '''

import copy
class OT_Char():
    def __init__(self, verbose="quiet"):
        # Verbose mode is for debugging purposes, not for production.
        # Default verbose is turned off.
        if verbose == "verbose":
            self.verbose = True
            print("-----> NEW CHARACTER TRANSFORM INITIATED <-----")
        else:
            self.verbose = False

    def convert_for_transform(self, op1, op2):
        ''' Used to convert raw operations from the client
         into readable dictonaries to allow for transform
         and readability. '''
        new_op_1 = {}
        new_op_2 = {}
        for j in op1:
            for i in j:
                if i == "retain":
                    op1_index = j[i]
                    new_op_1['index'] = op1_index
                if i == "insert":
                    op1_char = j[i]
                    new_op_1['insert'] = op1_char
                if i == "delete":
                    op1_del = j[i]
                    new_op_1['delete'] = op1_del

        for j in op2:
            for i in j:
                if i == "retain":
                    op2_index = j[i]
                    new_op_2['index'] = op2_index
                if i == "insert":
                    op2_char = j[i]
                    new_op_2['insert'] = op2_char
                if i == "delete":
                    op2_del = j[i]
                    new_op_2['delete'] = op2_del

        if self.verbose:
            print('---')
            print 'CONVERSIONS'
            print 'OP1:', op1, '--> OP1-Converted:', new_op_1
            print 'OP2:', op2, '--> OP2-Converted:', new_op_2
            print('---')
        return new_op_1, new_op_2

    def transform(self, op1, op2):
        ''' Control function, converts operations and
         assigns the operations to the appropriate transform '''

        # Use conversion function
        op1, op2 = self.convert_for_transform(op1, op2)

        # Throw the operations into sub functions
        transform_type = []
        if "insert" in op1:
            transform_type.append('Ins')
        elif "delete" in op1:
            transform_type.append('Del')
        if "insert" in op2:
            transform_type.append('Ins')
        elif "delete" in op2:
            transform_type.append('Del')

        if self.verbose:
            print 'TRANSFORM-TYPE'
            print transform_type

        # Send to sub-function depending on relationship
        if transform_type[0] == "Ins" and transform_type[1] == "Ins":
            transformed_ops = self.insert_insert(op1, op2, 1, 2), self.insert_insert(op2, op1, 2, 1)
        if transform_type[0] == "Del" and transform_type[1] == "Del":
            transformed_ops = self.delete_delete(op1, op2), self.delete_delete(op2, op1)
        if transform_type[0] == "Ins" and transform_type[1] == "Del":
            transformed_ops = self.insert_delete(op1, op2), self.delete_insert(op2, op1)
        if transform_type[0] == "Del" and transform_type[1] == "Ins":
            transformed_ops = self.delete_insert(op1, op2), self.insert_delete(op2, op1)

        if self.verbose:
            print('---')
            print 'TRANSFOMRED OPS'
            print 'OP1-PRIME:', transformed_ops[0]
            print 'OP2-PRIME:', transformed_ops[1]
            print('---')
            print("-----> END TRANSFORM TRANSMISSION <-----")

        return transformed_ops[0], transformed_ops[1]

    def insert_insert(self, op1, op2, order, order2):
        ''' Insert/Insert Relationship '''
        # Preserve op1, return's a transformed operation.
        # Execute after op2
        if op1['index'] < op2['index'] or (op1['index'] == op2['index'] and order > order2):
            op1_prime = op1
        else:
            op1['index'] = op1['index'] + 1
            op1_prime = op1

        return op1_prime

    def delete_delete(self, op1, op2):
        ''' Delete/Delete Relationship '''
        # Preserve op1, return's a transformed operation.
        # Execute after op2
        if op1['index'] < op2['index']:
            op1_prime = op1
        else:
            op1['index'] = op1['index'] - 1
            op1_prime = op1

        return op1_prime

    def insert_delete(self, op1, op2):
        ''' Insert/Delete Relationship '''
        # Preserve op1, return's a transformed operation.
        # Execute after op2
        if op1['index'] <= op2['index']:
            op1_prime = op1
        else:
            op1['index'] = op1['index'] - 1
            op1_prime = op1

        return op1_prime

    def delete_insert(self, op1, op2):
        ''' Delete/Insert Relationship '''
        # Preserve op1, return's a transformed operation.
        # Execute after op2
        if op1['index'] < op2['index']:
            op1_prime = op1
        else:
            op1['index'] = op1['index'] + 1
            op1_prime = op1

        return op1_prime



''' OT_String String-Wise Function '''
class OT_String():
    def __init__(self, verbose="quiet"):
        # Verbose mode is for debugging purposes, not for production.
        # Default verbose is turned off.
        if verbose == "verbose":
            self.verbose = True
            print("-----> NEW STRING TRANSFORM INITIATED <-----")
        else:
            self.verbose = False

    def convert_for_transform(self, op1, op2):
        ''' Used to convert raw operations from the client
         into readable dictonaries to allow for transform
         and readability. '''
        new_op_1 = {}
        new_op_2 = {}
        for j in op1:
            for i in j:
                if i == "retain":
                    op1_index = j[i]
                    new_op_1['index'] = op1_index
                if i == "insert":
                    op1_char = j[i]
                    new_op_1['insert'] = op1_char
                if i == "delete":
                    op1_del = j[i]
                    new_op_1['delete'] = op1_del
                if i == "operator":
                    op1_operator = j[i]
                    new_op_1['operator'] = op1_operator

        for j in op2:
            for i in j:
                if i == "retain":
                    op2_index = j[i]
                    new_op_2['index'] = op2_index
                if i == "insert":
                    op2_char = j[i]
                    new_op_2['insert'] = op2_char
                if i == "delete":
                    op2_del = j[i]
                    new_op_2['delete'] = op2_del
                if i == "operator":
                    op2_operator = j[i]
                    new_op_2['operator'] = op2_operator
        return new_op_1, new_op_2

    def transform(self, op1, op2):
        ''' Control function, converts operations and
         assigns the operations to the appropriate transform '''

        # Use conversion function
        op1, op2 = self.convert_for_transform(op1, op2)

        # Throw the operations into sub functions
        transform_type = []
        if "insert" in op1:
            transform_type.append('Ins')
        elif "delete" in op1:
            transform_type.append('Del')
        if "insert" in op2:
            transform_type.append('Ins')
        elif "delete" in op2:
            transform_type.append('Del')

        if self.verbose:
            print 'TRANSFORM-TYPE'
            print transform_type

        # Create unique 'copies' of the operations
        # Prevents variables from overriding eachother
        sop1 = copy.deepcopy(op1)
        sop2 = copy.deepcopy(op2)

        oop1 = copy.deepcopy(op1)
        oop2 = copy.deepcopy(op2)

        # Send to sub-function depending on relationship
        # Copies are always used in the second function
        if transform_type[0] == "Ins" and transform_type[1] == "Ins":
            transformed_ops = self.insert_insert(op1, op2), self.insert_insert(sop2, sop1)
        if transform_type[0] == "Del" and transform_type[1] == "Del":
            transformed_ops = self.delete_delete(op1, op2), self.delete_delete(sop2, sop1)
        if transform_type[0] == "Ins" and transform_type[1] == "Del":
            transformed_ops = self.insert_delete(op1, op2), self.delete_insert(sop2, sop1)
        if transform_type[0] == "Del" and transform_type[1] == "Ins":
            transformed_ops = self.delete_insert(op1, op2), self.insert_delete(sop2, sop1)

        if self.verbose:
            print('---')
            print 'TRANSFOMRED OPS'
            print 'OP1', oop1
            print 'OP2', oop2
            print 'OP1-PRIME:', transformed_ops[0]
            print 'OP2-PRIME:', transformed_ops[1]
            # Try check for segments. Only applicable to delete_insert operation
            try:
                if transformed_ops[0][1] != "" or transformed_ops[1][1] != "":
                    print 'FINAL-SEGMENT', transformed_ops[0][1]
            except:
                pass
            print("-----> END TRANSFORM TRANSMISSION <-----")

        return transformed_ops[0], transformed_ops[1]

    def insert_insert(self, op1, op2):
        ''' Insert/Insert Relationship '''
        # Preserve op1, return's a transformed operation.
        # Execute after op2
        if op1['index'] < op2['index']:
            op1_prime = op1
        else:
            op1['index'] = op1['index'] + (len(op2['insert']) - 1)
            op1_prime = op1

        return op1_prime


    def delete_delete(self, op1, op2):
        ''' Delete/Delete Relationship '''
        # Preserve op1, return's a transformed operation.
        # Execute after op2
        if op2['index'] >= (op1['index'] + op1['delete']):
            op1_prime = op1
        elif op1['index'] >= (op2['index'] + op2['delete']):
            op1['index'] = op1['index'] - op2['delete']
            op1_prime = op1
        else:
            if op2['index'] <= op1['index'] and (op1['index'] + op1['delete']) <= (op2['index'] + op2['delete']):
                op1['delete'] = 0
                op1_prime = op1
            elif op2['index'] <= op1['index'] and (op1['index'] + op1['delete']) > (op2['index'] + op2['delete']):
                op1['delete'] = op1['index'] + op1['delete'] - (op2['index'] + op2['delete'])
                op1['index'] = op2['index']
                op1_prime = op1
            elif op2['index'] > op1['index'] and (op2['index'] + op2['delete']) >= (op1['index'] + op1['delete']):
                op1['delete'] = op2['index'] - op1['index']
                op1_prime = op1
            else:
                op1['delete'] = op1['delete'] - op2['delete']
                op1_prime = op1
        return op1_prime

    def insert_delete(self, op1, op2):
        ''' Insert/Delete Relationship '''
        # Preserve op1, return's a transformed operation.
        # Execute after op2
        if op1['index'] <= op2['index']:
            op1_prime = op1
        elif op1['index'] > (op2['index'] + op2['delete']):
            op1['index'] = op1['index'] - op2['delete']
            op1_prime = op1
        else:
            op1['index'] = op2['index']
            op1_prime = op1

        return op1_prime

    def delete_insert(self, op1, op2):
        ''' Delete/Insert Relationship '''
        # Preserve op1, return's a transformed operation.
        # Execute after op2
        if op2['index'] >= (op1['index'] + op1['delete']):
            op1_prime = op1
        elif op1['index'] >= op2['index']:
            op1['index'] = op1['index'] + len(op2['insert'])
            op1_prime = op1
        else:
            # This is the only case where the operation needs to be segmented
            # because the two operations coexist and overlap, thus losing
            # convergence and neither intentions are preserved. The
            # first segment gets called first, then op2, then the second
            # segment gets called afterward.
            op1['delete'] = op2['index'] - op1['index']
            op1_prime = op1

            segment = {}
            segment['delete'] = op1['delete'] - (op2['index'] - op1['index'])
            segment['index'] = op2['index'] + len(op2['insert'])
            return op1_prime, segment

        return op1_prime


'''
DEL/INS OVERLAP STRING EXAMPLE

op1 = [{"retain": 1}, {"delete": 4}]
op2 = [{"retain": 3}, {"insert": "op"}]

OTC = OT_String("verbose")
new_ops = OTC.transform(op1, op2)
'''

'''
INS/INS STRING EXAMPLE
op1 = [{"retain": 2}, {"insert": "wow"}]
op2 = [{"retain": 4}, {"insert": "op"}]

OTC = OT_String("verbose")
new_ops = OTC.transform(op1, op2)
'''

'''
DEL/DEL STRING EXAMPLE

op1 = [{"retain": 1}, {"delete": 2}]
op2 = [{"retain": 2}, {"delete": 3}]

OTC = OT_String("verbose")
new_ops = OTC.transform(op1, op2)
'''
