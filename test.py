reference = 'cactaagcacacagagaataatgtctagaatctgagtgccatgttatcaaattgtactgagactcttgcagtcacacaggct'
pattern_list = ['acac']
pattern_list_2 = ['*BIOTIN*-ACAC', 'TGTC', 'aaa', 'act gag act ctt gc']
query_dict = {}
pattern_lengths = ''
for pattern in pattern_list:
    pattern_lengths += str(len(pattern))
    print('test')