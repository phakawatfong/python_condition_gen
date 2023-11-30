from configparser import ConfigParser
import ast
import os

current_dir=os.getcwd()
output_path=f"{current_dir}/output"
config_path=f"{current_dir}/config"

config = ConfigParser()
config.read(f"{config_path}/configfile.txt")


date_list = ast.literal_eval(config.get("INPUT_PARAM", "date_list"))
num_list = ast.literal_eval(config.get("INPUT_PARAM", "num_list"))
COL_NAME=config.get("INPUT_PARAM", "COL_NAME")

MIN_RANGE=int(config.get("INPUT_PARAM", "MIN_RANGE"))
MAX_RANGE=int(config.get("INPUT_PARAM", "MAX_RANGE"))


val_interval=list()
print("date_list_len",len(date_list))
print("num_list_len",len(num_list))

where_string=""

sum_num=0
i=1

kv_dict=dict()
first_index=0
last_index=0
counter=0
for val in num_list:
    sum_num+=val
    counter+=1
    

    if sum_num >= MIN_RANGE and sum_num < MAX_RANGE and first_index==last_index and (first_index!=0 and last_index!=0):
        last_index=counter-1
        # print(f"first_index={first_index}, last_index={last_index}")
        kv_dict[sum_num]=(first_index, last_index)
        sum_num=0
    
        first_index=last_index+1
    
    elif sum_num >= MAX_RANGE:
        last_index=counter-1
        # print(f"first_index={first_index}, last_index={last_index}")
        kv_dict[sum_num]=(first_index, last_index)
        sum_num=0
    
        first_index=last_index+1

    elif sum_num < MAX_RANGE and counter==len(num_list):
        last_index=counter-1
        kv_dict[sum_num]=(first_index, last_index)
        sum_num=0

# print(kv_dict)
        

index_list=[]
for key,val in kv_dict.items():
    val=list(val)
    index_list.append(val)


# print(index_list)

condition_list=[]

for pair_ind in index_list:
    my_string=""
    val_1, val_2 = pair_ind

    if val_1 == val_2:
        my_string+=f"{COL_NAME} = -min \"{date_list[val_1]}\""
        condition_list.append(my_string)
        # my_string=""

    else:
        my_string+=f"{COL_NAME} between date'{date_list[val_1]}' and date'{date_list[val_2]}'"
        condition_list.append(my_string)
        # my_string=""

# print(condition_list)


for val in condition_list:
    print(val)

for key,value in kv_dict.items():
    print(key)


with open(f"{output_path}/condition_output_file.txt", "w") as file:
    for val in condition_list:
        file.write(val + "\n")

with open(f"{output_path}/record_output_file.txt", "w") as file:
    for key,value in kv_dict.items():
        file.write(str(key) + "\n")