"""
-------------------------------------------------------
Apriori.py
[program description]
-------------------------------------------------------
"""
import itertools
import sys
def is_subset(set1,set2):
    #checks if set2 is a subset of set1
    subset=True
    for i in set2:
        if i not in set1:
            subset=False
            break
    return subset
def find_freq(itemsets,candidates,support):
    frequent_set=[]
    counts=[]
    for c_set in candidates:
        count=0
        #count how many item sets the canndidate set appears in
        for i_set in itemsets:
            if is_subset(i_set, c_set):
                count+=1
        
        if count>=support:
            counts.append(count)
            frequent_set.append(c_set)
    return frequent_set, counts
        
def make_pair_rule(x,y,singles,s_count,p_count,pairs):
    rule=str(x)+" -> "+str(y)
    #get previously stored counts for pair and single item
    pair_count=find_count((x,y),pairs,p_count)
    single_count=find_count(x,singles,s_count)
    confidence=pair_count/single_count
    return rule,confidence

def find_count(item,items_list,counts):
    if(item in items_list):
        i=items_list.index(item)
    else:
        i=items_list.index((item[1],item[0]))#may have to reverse the pair
    return counts[i]

def create_triples(freq_pairs):
    triples=[]
    for p1 in freq_pairs:
        for p2 in freq_pairs:
            if(p1[0]==p2[0]):
                trip_same=(p1[0],p2[1],p1[1])
                
                if(trip_same not in triples and p1[0]!=p1[1]!=p2[1]):
                    triples.append((p1[0],p1[1],p2[1]))
    return triples

def label_items(lables,items):
    i=0
    for it in items:
        items[i]=lables[i]+": "+items[i]
        i+=1
    return items
        
def main(): 
    
    f=open("StudentsPerformanceBinned.csv","r")
    NUM_OF_REC=1000
    support_pec=10/100#10% support by default
    #get support and min confidence value from cmd line
    min_confidence=0
    if(len(sys.argv)>1):
        support_pec=int(sys.argv[1])/100
    if(len(sys.argv)>2):
        min_confidence=float(sys.argv[2])
    

    support=NUM_OF_REC*support_pec
    #print(support, min_confidence)

    all_itemset=[]
    all_items=[]
    line_num=0
    lables=[]
    for line in f:
        items=line.strip().split(",")
        
        if line_num!=0:
            items=label_items(lables,items)
            all_itemset.append(items)
            
            #put all items in a list
            for i in items:
                if i not in all_items:
                    all_items.append(i)
        else:
            #take first row as lables
            lables=items
        line_num+=1
    
    all_items.sort()
    
    print("File parsed...")
    
    single_counts=[]
    #prune out in frequent items 
    index=0;
    while(index<len(all_items)):
        i=all_items[index]
        count=0
        for set in all_itemset:
            if i in set:
                count+=1
    
        if count<support:
            all_items.remove(i)
        else:
            single_counts.append(count)
            index+=1
    
    print("Singles pruned...")
    #create pairs
    candidates=list(itertools.combinations(all_items,2))
    #get frequent pairs
    print("Candiate pairs create")
    freq_pairs,pair_counts=find_freq(all_itemset, candidates, support)
    print("Pairs created and pruned...")
    rules=[]
    con_lev=[]
    for pair in freq_pairs:
        #get rules and their confidence levels
        rule,con=make_pair_rule(pair[0], pair[1], all_items, single_counts, pair_counts, freq_pairs)
        rules.append(rule)
        con_lev.append(con)
        rule,con=make_pair_rule(pair[1], pair[0], all_items, single_counts, pair_counts, freq_pairs)
        rules.append(rule)
        con_lev.append(con)
        
    #sort rules based on confidence
    sorted_rules=[rules for _,rules in sorted(zip(con_lev,rules),reverse=True)]
    con_lev.sort(reverse=True)
    #prepare file for printing
    f=open("ariori_results_s"+str(support_pec*100)+".csv","w+")

    f.write("Rules, confidence\n")
    for i in range(0,len(con_lev)):
        if con_lev[i]>=min_confidence:
            print(sorted_rules[i]," Confidence: "+str(con_lev[i]))
            f.write(str(sorted_rules[i])+", "+str(con_lev[i])+"\n")
        
    #create triples  
    candidates=create_triples(freq_pairs)
    freq_trip,trip_counts=find_freq(all_itemset, candidates, support)
    print()
    print("Triples")
    f.write("Triples rules:\n")
    rules=[]
    con_lev=[]
    for trip in freq_trip:
        #get triplet count
        t_count=find_count(trip, freq_trip, trip_counts)
        pair=(trip[0],trip[1])
        pair_count=find_count(pair, freq_pairs, pair_counts)
        rules.append(str(pair)+" -> "+str(trip[2]))
        #calculate confidence 
        con_lev.append(t_count/pair_count)
        
        pair=(trip[0],trip[2])
        pair_count=find_count(pair, freq_pairs, pair_counts)
        rules.append(str(pair)+" -> "+str(trip[1]))
        #calculate confidence 
        con_lev.append(t_count/pair_count)
        
        pair=(trip[1],trip[2])
        pair_count=find_count(pair, freq_pairs, pair_counts)
        rules.append(str(pair)+" -> "+str(trip[0]))
        #calculate confidence 
        con_lev.append(t_count/pair_count)
        
    
    #sort rules based on confidence
    sorted_rules=[rules for _,rules in sorted(zip(con_lev,rules),reverse=True)]
    con_lev.sort(reverse=True)
    for i in range(0,len(con_lev)):
        if con_lev[i]>=min_confidence:
            rule=sorted_rules[i]
            rule=rule.replace("'","")
            print(rule," Confidence: "+str(con_lev[i]))
            f.write('"'+rule+"\", "+str(con_lev[i])+"\n")#print to csv, need to wrap rule in quotes because of comma
        
main() 