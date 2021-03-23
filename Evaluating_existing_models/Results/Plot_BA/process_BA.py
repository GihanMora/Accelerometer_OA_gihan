import os
path = "E:\Projects\Accelerometer_OA_gihan\Evaluating_existing_models\Results\Plot_BA\\mont_17\\"

files_list = os.listdir(path)

for k in files_list:
    if(k[-4:]=='.txt'):
        f = open(path+k,'r')
        lines = f.readlines()
        print(lines[2].strip().split('/')[-1])
        print(lines[3].strip().split(':'))
        print(lines[4].strip().split(':'))
        print(lines[5].strip().split(':'))
        print(lines[4].strip().split(':')[1]+' ('+lines[5].strip().split(':')[1]+'-'+lines[3].strip().split(':')[1]+')')
        print()
        print()