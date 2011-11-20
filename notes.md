## Notes for Link Analysis
# PageRank
graph.txt has X lines of text where each line is in the form "<email id> <sender email> <receiver email>"
Number of unique...
* IDs: 242047
* senders: 19802
* receivers: 77660
* senders+receivers: 86293

For nodes on the graph it is likely that we use s+r.
Some emails are malformed, though the task description indicates we should completely ignore them and consider them normal.
We are to ignore any links of the for A->A. If the node A only emails itself it becomes a 'freestanding' node and is excluded from the N count.

# Hubs and Authorities
The slides indicate to calculate the hubs first, then authorities.
The hubs and authorities algorithm gets the sanity check numbers on the 9th iteration.
Though the numbers are slightly different on the 10th iteration. This may be due to float point arithmetic or other flaw in the code. However the code is fairly straight forward and I cannot see what's wrong.
I suggest using both 9 and 10 iterations for 

# Sanity checks
kate.symes@enron.com:
* 0.00174604 -- pagerank L1-normalised 
* 0.00017473 -- pagerank unnormalised
* 0.00401388 -- hub score
* 0.06632742 -- authority score

jeff.dasovich@enron.com:
* 0.00100596 -- hub score 
* 0.00021004 -- authority score
* 0.00060603 -- pagerank unnormalised
* 0.00373347 -- pagerank L1-normalised