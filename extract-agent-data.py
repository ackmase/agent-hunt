import csv
import os
import re
import sys
import time
import urllib


AGENT_ID_KEY = 'AgentIds'
AGENT_NAME_KEY = 'AgentName'
AGENT_URL_KEY = 'AgentUrl'

AGENT_FILE_NAME = '%s.html'
AGENT_IDS_FILE_NAME = 'agents.csv'
AGENT_URL = 'http://www.publishersmarketplace.com/members/%s/'
OUTPUT_FILE_NAME = 'output.csv'


class Agent(object):
  
  def __init__(self, agent_id, path_to_dir, download):
    self.agent_id = agent_id
    self.path_to_dir = path_to_dir
    self.download = download
    self.path_to_file = os.path.join(path_to_dir, AGENT_FILE_NAME % agent_id)
    self.agent_url = AGENT_URL % agent_id
    self.agent_name = None
    self.agency = None
    self.picture_books = False
    
  def ExtractData(self):
    if self.download:
      time.sleep(1)
      urllib.urlretrieve(self.agent_url, self.path_to_file)
    
    with open(self.path_to_file, 'r') as f:
      for row in f:
        for re_groups in re.findall(r'(<title>Publishers Marketplace: )([\w.,\-&\'\s]+)(<\/title>)', row):
          self.agent_name = re_groups[1]
          
  def ToDict(self):
    return {AGENT_NAME_KEY: self.agent_name,
            AGENT_ID_KEY: self.agent_id,
            AGENT_URL_KEY: self.agent_url}
            
          
def GetAgentIdsFromCsv(path_to_dir):
  path_to_file = os.path.join(path_to_dir, AGENT_IDS_FILE_NAME)
  
  with open(path_to_file, 'r') as f:
    csv_reader = csv.DictReader(f)
    for row in csv_reader:
      yield row[AGENT_ID_KEY]
      
def WriteToCsv(agents):
    to_write = [agent.ToDict() for agent in agents]
    example_agent = agents.pop()
    output_file_path = os.path.join(example_agent.path_to_dir, OUTPUT_FILE_NAME)
    
    with open(output_file_path, 'w') as f:
      csv_writer = csv.DictWriter(f, fieldnames=example_agent.ToDict())
      csv_writer.writeheader()
      csv_writer.writerows(to_write)

def main():
  if len(sys.argv) != 3:
    print 'usage: python extract_agent_data.py /path/to/dir download?'

  path_to_dir = sys.argv[1]
  download = True if sys.argv[2] == 'True' else False

  agent_ids = GetAgentIdsFromCsv(path_to_dir)
  agents = [Agent(agent_id, path_to_dir, download) for agent_id in agent_ids]
  
  # Extract Data.
  [agent.ExtractData() for agent in agents]
  
  WriteToCsv(agents)

if __name__ == '__main__':
  main()
