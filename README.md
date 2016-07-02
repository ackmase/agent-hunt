# agent-hunt
Modules for finding agent member IDs and extracting data from agent member pages. 

Start with get-agent-ids.py which will allow you to query the database and find members who have been marked as agents. Once you've collected the agent IDs, copy and paste them into a CSV with the column name, AgentId. Feed that CSV into extract-agent-data.py which will extract various pieces of information from the individual agent pages and drop them into an output CSV.
