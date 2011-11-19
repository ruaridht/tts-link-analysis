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