def print_matrix(coeff_m):
    for i in range(len(coeff_m)):
            print(coeff_m[i])



def valid_check(matrix):
    if type(matrix) != list:
        return False

    for i in range(len(matrix)):
        if len(matrix[i]) != len(matrix[i-1]) or type(matrix[i]) != list:
            return False 
        
        for j in range(len(matrix[i])):
            if type(matrix[i][j]) != float and type(matrix[i][j]) != int:
                return False
    return True
    


def rectangle_check(matrix):
    for i in range(len(matrix)):
        if len(matrix[i]) != len(matrix[i-1]):
            return False
    return True



def square_check(matrix):
    for row in matrix:
        if len(row) != len(matrix):
            return False
    return True



def row_switch(coeff_m, row1, row2):
    if not rectangle_check(coeff_m):
        raise ValueError('coeff_m is not a rectangle')
    
    new_m = []
    for row in coeff_m:
        if row == row1:
            new_m.append(row2)
            
        elif row == row2:
            new_m.append(row1)
        
        else:
            new_m.append(row)
            
    return new_m



def row_amplifier(row, multiplier):
    row_amped = []
    for x in row:
        row_amped.append(x * multiplier)
    return row_amped



def row_add(row1, row2):
    if len(row1) != len(row2):
        raise ValueError('rows need to be the same length')
    new_row = []
    for i in range(len(row1)):
        new_row.append(row1[i] + row2[i])
    
    return new_row



def row_subtract(row1, row2):
    if len(row1) != len(row2):
        raise ValueError('rows need to be the same length')
    new_row = []
    for i in range(len(row1)):
        new_row.append(row1[i] - row2[i])
    
    return new_row



def variable_creator(coeff_m):
    var_list = []
    for i in range(len(coeff_m)):
        var_list.append(f'x{i+1}')
    
    var_dict = dict.fromkeys(var_list, 0)
    return var_dict
        


def row_reduction(coeff_m, sln_m):
    
    i = 0
    if not valid_check(coeff_m) or not valid_check(sln_m):
        raise ValueError('one or both of the matrices are invalid')
    if len(coeff_m) != len(sln_m):
        raise ValueError('matrices are not the same size')
    if not rectangle_check(coeff_m) or not rectangle_check(sln_m):
        raise ValueError('coeff or sln matrix are not rectangular')

    while i < len(coeff_m):
        for target_row in range(len(coeff_m)):


            if coeff_m[target_row][i] == 0:
                for row in range(target_row + 1, len(coeff_m)):
                    if coeff_m[row][i] != 0:
                        coeff_m = row_switch(coeff_m, coeff_m[target_row], coeff_m[row])
                        sln_m = row_switch(sln_m, sln_m[target_row], sln_m[row])
                        break


            sln_m[target_row] = row_amplifier(sln_m[target_row], 1/(coeff_m[target_row][i]))
            coeff_m[target_row] = row_amplifier(coeff_m[target_row], 1/(coeff_m[target_row][i]))
            
            print(sln_m[target_row])
            print(coeff_m[target_row])
            print('\n')


            for row in range(len(coeff_m)):
                if coeff_m[row] != coeff_m[target_row] and sln_m[row] != sln_m[target_row]:
                    if coeff_m[row][i] > 0:
                        sln_m[row] = row_subtract(sln_m[row], row_amplifier(sln_m[target_row], coeff_m[row][i]))
                        coeff_m[row] = row_subtract(coeff_m[row], row_amplifier(coeff_m[target_row], coeff_m[row][i]))

                    elif coeff_m[row][i] < 0:
                        sln_m[row] = row_add(sln_m[row], row_amplifier(sln_m[target_row], abs(coeff_m[row][i])))
                        coeff_m[row] = row_add(coeff_m[row], row_amplifier(coeff_m[target_row], abs(coeff_m[row][i])))
                
                if coeff_m[row].count(0) == len(coeff_m[row]) and sln_m[row] == [0]:
                    return 'there is a free variable(s), the augmented matrix is outside the scope of this code' 
                elif coeff_m[row].count(0) == len(coeff_m[row]) and sln_m[row] != [0]:
                    raise ValueError('no solution')

            print_matrix(coeff_m)
            print_matrix(sln_m)
            print('\n')

        
            i += 1
            
        return sln_m



def solve(coeff_m, sln_m):
    '''(list<list<float>>, list<list<float>>) -> dict<float>'''
    var_dict = variable_creator(coeff_m)
    final_sln_m = row_reduction(coeff_m, sln_m)
    
    if type(final_sln_m) != list:
        return final_sln_m
    
    count = 0
    for key in var_dict:
        var_dict[key] = final_sln_m[count][0]
        count += 1
        
    return var_dict



def lower_triangular(coeff_m):
    if not square_check(coeff_m) or len(coeff_m) < 2 or not valid_check(coeff_m):
        raise ValueError('invalid matrix')
    

    i = 0
    while i < len(coeff_m):
        for target_row in range(len(coeff_m)):

            if coeff_m[target_row][i] == 0:
                for row in range(target_row + 1, len(coeff_m)):
                    if coeff_m[row][i] != 0:
                        coeff_m[target_row] = row_switch(coeff_m, coeff_m[target_row], coeff_m[row])

            if target_row == len(coeff_m) - 1:
                i += 1
                continue

            
            print(coeff_m[target_row])
            print('\n')


            for row in range(target_row +1, len(coeff_m)):

                if coeff_m[row][i] > 0:
                    coeff_m[row] = row_subtract(coeff_m[row], row_amplifier(coeff_m[target_row], coeff_m[row][i]/(coeff_m[target_row][i])))

                elif coeff_m[row][i] < 0:
                    if coeff_m[target_row][i] < 0:
                        coeff_m[row] = row_subtract(coeff_m[row], row_amplifier(coeff_m[target_row], abs(coeff_m[row][i]/(coeff_m[target_row][i]))))
                    elif coeff_m[target_row][i] > 0:
                        coeff_m[row] = row_add(coeff_m[row], row_amplifier(coeff_m[target_row], abs(coeff_m[row][i]/(coeff_m[target_row][i]))))
            
            print_matrix(coeff_m)
            print('\n')

            i += 1

    return coeff_m



def determinant(coeff_m):
    lt_matrix = lower_triangular(coeff_m)

    det = 1
    for i in range(len(lt_matrix)):
        det *= lt_matrix[i][i]

    return det



def inverse(coeff_m):
    if determinant(coeff_m) == 0: 
        raise ValueError('this matrix is singular meaning it does not have an inverse')
    elif not valid_check(coeff_m) or not square_check(coeff_m):
        raise ValueError('invalid matrix')

    identity = []
    for row in range(len(coeff_m)):
        row_list = []
        for col in range(len(coeff_m)):
            if row == col:
                row_list.append(1)
            else:
                row_list.append(0)
        identity.append(row_list)       
        

    return row_reduction(coeff_m, identity)



def column_replacement(coeff_m, col, index):

    for i in range(len(col)):
        if len(col[i]) != 1:
            raise ValueError('this entry does not correspond to a column of values')

    mod_m = []
    for i in range(len(coeff_m)):
        row = []
        for j in range(len(coeff_m)):
            if j == index:
                row.append(col[i][0])
            else:
                row.append(coeff_m[i][j])

        mod_m.append(row)
    
    return mod_m



def cramers(coeff_m, sln_m, target_var):
    if not valid_check(coeff_m):
        raise ValueError('invalid matrix')
    elif not square_check(coeff_m):   
        raise ValueError('the coefficient matrix must be a square')

    mod_coeff_m = column_replacement(coeff_m, sln_m, target_var)
    
    if determinant(coeff_m) == 0:\
        raise ZeroDivisionError('determinant of the coeff matrix is 0')
    else:
        return determinant(mod_coeff_m)/determinant(coeff_m)



def multiplication(matrix1, matrix2):
    if not valid_check(matrix1) and not rectangle_check(matrix1) or not valid_check(matrix2) and not rectangle_check(matrix2):
        raise ValueError('one or both of these matrices is not a proper matrix')
    
    if len(matrix2) != len(matrix1[0]):
        raise ValueError('matrix multiplication cannot be performed on these two matrices')
    
    product = []
    for i in range(len(matrix1)):
        temp_row = []
        for col in range(len(matrix2[0])):
            sum = 0
            for row in range(len(matrix1)):
                sum += matrix1[i][row]*matrix2[row][col]
            temp_row.append(sum)
        product.append(temp_row)
            

    return product



def transpose(matrix):
    if not valid_check(matrix) or not rectangle_check(matrix):
        raise ValueError('invalid matrix')
    new_m = []
    for i in range(len(matrix)):
        temp_row = []
        for j in range(len(matrix[i])):
            temp_row.append(matrix[j][i])
        new_m.append(temp_row)
    
    return new_m



def trace(matrix):
    if not valid_check(matrix) or not square_check(matrix):
        raise ValueError('invalid matrix')
    
    total = 0
    for i in range(len(matrix)):
        total += matrix[i][i]
    
    return total



def matrix_add_sub(matrix1, matrix2, operation):
    if not valid_check(matrix1) and not rectangle_check(matrix1) or not valid_check(matrix2) and not rectangle_check(matrix2):
        raise ValueError('one or both of these matrices is not a proper matrix')
        
    if len(matrix1) != len(matrix2):
        raise ValueError('these matrices do not have the same number of rows')

    new_m = []
    for i in range(len(matrix1)):
        if len(matrix1[i]) != len(matrix2[i]):
            raise ValueError(f'invalid row at row{i+1}')
        if 'add' in operation.lower():
            new_m.append(row_add(matrix1[i], matrix2[i]))
        elif 'subtract' in operation.lower():
            new_m.append(row_subtract(matrix1[i], matrix2[i]))
        else:
            raise AssertionError('invalid operation input')


    return new_m


