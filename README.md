# TTS Practical 4
Ruaridh Thomson

## Specification
The year is 2001 and you are helping the US Securities and Exchange Commission investigate the scandal surrounding the Enron Corporation. The SEC has secured access to all communications of the relevant persons, but they are having a hard time understanding the flow of information within the company. Your goal is to analyse the pattern of email communications and discover who emails whom and why. You decide to treat employees as nodes in the social graph and emails as links between them. Any time person A sends an email to person B, you will interpret this as a directed link from A to B. Emails that have more than one recipient should count as several directed links, one for each recipient. For example, if person A sends an email to persons B and C, you have two directed links: A→B and A→C. Repeated links should count multiple times. In other words, if A emails B ten times, you should treat A→B as ten identical links (or as a link with a weight of 10). Links of the form A→A (i.e. emails sent to oneself) should be excluded from the graph.

## Tasks
* Implement PageRank, Hubs and Authorities algorithms.
* Save the top ten scores for each.
* End
