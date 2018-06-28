# THINGS TO DO

# Isolates + Member + Star < Bridge < Organizer

import networkx as nx
from community import community_louvain
import pandas as pd
import operator

# ORGANIZER/LIAISON/BROKER
G = nx.read_weighted_edgelist('Only_50_Employees1.csv', delimiter=',', create_using = nx.DiGraph(), nodetype=str)
page_score = dict(nx.pagerank(G))
eigen_score = dict(nx.eigenvector_centrality(G))
betweenness_score = dict(nx.betweenness_centrality(G))
mydicts = [page_score, betweenness_score, eigen_score]
df = pd.concat([pd.Series(d) for d in mydicts], axis=1).fillna(0).T
df.index = ['page_score', 'betweenness_score', 'eigen_score']
df = df.transpose()
del page_score, eigen_score, betweenness_score, mydicts
df = (df - df.mean()) / (df.max() - df.min())
minus_columns = ['page_score', 'betweenness_score', 'eigen_score']
df = df[minus_columns] + 1
df['score'] = df['page_score'] + df['betweenness_score'] + df['eigen_score']
del df['page_score'], df['betweenness_score'], df['eigen_score']
score_dict = df['score'].to_dict()
n = int(len(score_dict) * 0.10)
organizer_dict = dict(sorted(score_dict.items(), key=operator.itemgetter(1), reverse=True)[:n])
organizer_dict = {x: 0 for x in organizer_dict}
del score_dict, df, n, minus_columns



# BRIDGE/GATEKEEPER
G = nx.read_weighted_edgelist('Only_50_Employees1.csv', delimiter=',', create_using = nx.Graph(), nodetype=str)
gatekeeper = dict(nx.bridges(G))
gatekeeper_dict = {k: v for k, v in gatekeeper.items() if k not in organizer_dict}
gatekeeper_dict = {x: 1 for x in gatekeeper_dict}
del gatekeeper



# STAR/TEAM-PLAYER
G = nx.read_weighted_edgelist('Only_50_Employees1.csv', delimiter=',', create_using = nx.Graph(), nodetype=str)
part = community_louvain.best_partition(G)                                                     # Finding Communities
invert_partition = {v: k for k, v in part.items()}
star_dict = {}        # iterate over each community
for community_id in invert_partition.keys():                                                   #Extract the sub graph containing the community nodes
    temp_graph = G.subgraph(invert_partition[community_id])
    temp_degree = dict(temp_graph.degree())                                                    #Extract the degrees in the subgraph
    star_dict[community_id] = max(temp_degree, key=lambda x: temp_degree[x])                   #Store it in a dictionary, with key as community_id and value as the node with max degree
star_dict = dict((v,k) for k,v in sorted(star_dict.items(), key=operator.itemgetter(1)))
star_dict = {k: v for k, v in star_dict.items() if k not in organizer_dict}
star_dict = {k: v for k, v in star_dict.items() if k not in gatekeeper_dict}
star_dict = {x: 2 for x in star_dict}
del community_id, invert_partition, part, temp_degree



# ISOLATES
isolate_dict = dict(G.degree())
isolate_dict = {key:val for key, val in isolate_dict.items() if val == 1 or 0}
isolate_dict = {x: 3 for x in isolate_dict}



# Integration of Final Appointed Roles
final_roles = {**organizer_dict, **gatekeeper_dict, **star_dict, **isolate_dict}
del organizer_dict, gatekeeper_dict, star_dict, isolate_dict















