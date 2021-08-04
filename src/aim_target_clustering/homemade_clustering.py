import util



if __name__ == '__main__':
    
    targets = util.create_dataset()
    clusters = util.basic_greedy_clustering(targets, MIN_COST_PER_METER_WELL=1)
    total_value = 0
    final_clusters = []
    while len(clusters) != 0:
        cluster, value = util.try_all_target_combinations(clusters.pop())
        if value != 0:
            if len(cluster) > 1:
                final_clusters = final_clusters + cluster
            else:
                final_clusters.append(cluster)
            total_value += value
    print('value', total_value)
    for cluster in final_clusters:
        print('cluster:  [ ')
        # for e in cluster:
        #     #print(" ",e['id'], e['value'], end = ' ')
        #     print(e)
        print(cluster)
        print(' ]')
