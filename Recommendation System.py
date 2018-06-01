# This recommendation system is based on giving points to each product ,  through three layers:
# 1st layer - Main Category, 2nd - Sub Category of product , 3rd - Product
# Points is given to each product based on keyword search.
classif = open('product_dataset.txt','r').read()
temp = classif.split('\n')
# 0 index has Main Category, 1 has sub category and 2 has products
main_data = temp[0].split(';')
temp_sub = temp[1].split(';')
sub_data = []
for each in temp_sub:
    sub_data.append(each.split(','))
temp_prod1 = temp[2].split(';')
prod_data = []
for i in temp_prod1:
    temp_prod2 = i.split(',')
    prod1 = []
    for j in temp_prod2:
        prod1.append(j.split(' '))
    prod_data.append(prod1)

def give_points(array,query,init_score=[0]): # query is a single string
    length = len(array)
    query_split = query.split(' ')
    if init_score == [0]:
        init_score = [0]*length
    for i in range(0,length):
        if array[i] in query_split:init_score[i]+=1
    return init_score

def give_points_sub(array,query,init_score=[0]):
    new_score = []
    l = len(array)
    if not init_score==[0]:
        for each in range(0,l): 
            new_score.append(give_points(array[each],query,init_score[each]))
    else:
        for each in range(0,l): 
            new_score.append(give_points(array[each],query,init_score))
    
    return new_score
def give_points_prod(array,query,init_score=[0]):
    new_score = []
    l = len(array)
    if not init_score==[0]:
        for each in range(0,l):
            new_score.append(give_points_sub(array[each],query,init_score[each]))
    else:
        for each in range(0,l):
            new_score.append(give_points_sub(array[each],query,init_score))
        
    return new_score

def point_assign(main,sub,item,query_list): # assigns points to each layer
    l = len(query_list)
    first = query_list[0]
    main_points = give_points(main,first)
    sub_points = give_points_sub(sub,first)
    item_points = give_points_prod(item,first)
    for each in range(1,l):
        main_points = give_points(main,query_list[each],main_points)
        sub_points = give_points_sub(sub,query_list[each],sub_points)
        item_points = give_points_prod(item,query_list[each],item_points)
    return [main_points,sub_points,item_points]

def main_to_sub(main_points,sub_points):
    l_main = len(main_points)
    for i in range(0,l_main):
        l_sub = len(sub_points[i])
        for j in range(0,l_sub):
            sub_points[i][j]=sub_points[i][j]+main_points[i]
    return sub_points
#prod_to_sub is to assign similar products higher points
def prod_to_sub(prod_points,sub_points):
    l_sub = len(sub_points)
    for i in range(0,l_sub): #[a,b] i = 0
        l_sub1 = len(sub_points[i])
        for j in range(0,l_sub1):# a j = 0
            l_prod = len(prod_points[i][j])
            sub_points[i][j]+=sum(prod_points[i][j])
    return sub_points
    
def sub_to_prod(sub_points,prod_points):
    l_sub = len(sub_points)
    for i in range(0,l_sub): #[a,b] i = 0
        l_sub1 = len(sub_points[i])
        for j in range(0,l_sub1):# a j = 0
            l_prod = len(prod_points[i][j])
            for k in range(0,l_prod):
                prod_points[i][j][k]+=sub_points[i][j]
    return prod_points

def make_both_linear(product_names,product_points): # since the product array is not in linear format, this function changes it to linear format
    names = []
    points =[]
    l_prod = len(product_names)
    for i in range(0,l_prod):
        l_prod1 = len(product_names[i])
        for j in range(0,l_prod1):
            l_prod2 = len(product_names[i][j])
            for k in range(0,l_prod2):
                points.append(product_points[i][j][k])
                names.append(product_names[i][j][k])
    return [names,points]

def top_n(name,value,n):
    descending = sorted(value,reverse=True)
    sliced=descending[0:n]
    l = len(value)
    name_list=[]
    for each in sliced:
        for i in range(0,l):
            if each==value[i] and not name[i] in name_list:
                name_list.append(name[i])
                break
    return name_list


query_list = ['Top laptop','mac price','table for laptop']
tot_score = point_assign(main_data,sub_data,prod_data,query_list)
new_sub_score=main_to_sub(tot_score[0],tot_score[1])
new_sub_score=prod_to_sub(tot_score[2],new_sub_score)
final_product_score = sub_to_prod(new_sub_score,tot_score[2])
result = make_both_linear(prod_data,final_product_score)
print('Recommended Products: ',top_n(result[0],result[1],8))