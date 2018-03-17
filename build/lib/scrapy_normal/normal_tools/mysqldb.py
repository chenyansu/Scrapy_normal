# -*- coding: UTF-8 -*-
from collections import OrderedDict

item = {"a":1, "b":2, "c":3, "d":4}


table_name = "spider_XXX"

part1 = "insert into "
part2 = table_name
part3 = "("
item_key_list= []
for k in item.keys():
    item_key_list.append(k)
part4 = str(item_key_list).replace("[", "").replace("]", "")
part5 = ") Values ("
for s in range(len(item)):
    part5 += "%s, "
part6 = ")"

cmd = part1+part2+part3+part4+part5+part6
print(cmd)

# item_list  = []
# for v in item_o.values():
#     item_list.append(v)
# item_tuple = tuple(item_list)
# print(item_tuple)

item_value_list = []
for i in item_key_list:
    item_value_list.append(item[i])
item_value_tuple = tuple(item_value_list)
print(item_value_tuple)