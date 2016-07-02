import csv
import os
import re
import sys
import time
import urllib


AGENCY_KEY = 'Agency'
AGENT_ID_KEY = 'AgentIds'
AGENT_NAME_KEY = 'AgentName'
AGENT_URL_KEY = 'AgentUrl'
PICTURE_BOOK_KEY = 'PictureBook'

AGENT_FILE_NAME = '%s.html'
AGENT_IDS_FILE_NAME = 'agents.csv'
AGENT_URL = 'http://www.publishersmarketplace.com/members/%s/'
OUTPUT_FILE_NAME = 'output.csv'


class Agent(object):
  """Object that holds data for a single agent. 
  
  Methods:
    ExtractData: Extracts data from the agent's individual page.
    ToDict: Converts agent object into a dictionary.
  """
  
  def __init__(self, agent_id, path_to_dir, download):
    """Initializes agent object.
    
    Args:
      agent_id: str, agent ID.
      path_to_dir: str, path to directory for storing agent page html and the output CSV.
      download: boolean, whether to download the agent html pages. Set to false if the 
        html files have already been downloaded and the object can access the file 
        directly without downloading.
    """
    self.agent_id = agent_id
    self.path_to_dir = path_to_dir
    self.download = download
    self.path_to_file = os.path.join(path_to_dir, AGENT_FILE_NAME % agent_id)
    self.agent_url = AGENT_URL % agent_id
    self.agent_name = None
    self.picture_books = False
    self.agency = None
    
    # Following variables are stubs and aren't currently extracted.
    self.website_url = None
    
  def ExtractData(self):
    """Extract data from individual agent pages."""
    # Only download html page if requested.
    if self.download:
      time.sleep(1)
      urllib.urlretrieve(self.agent_url, self.path_to_file)
    
    with open(self.path_to_file, 'r') as f:
      for row in f:
        # Extract agent name.
        for re_groups in re.findall(r'(<title>Publishers Marketplace: )([\w.,\-&\'\s]+)(<\/title>)', row):
          self.agent_name = re_groups[1]
          
        # Extract agency.
        for re_groups in re.findall(r'(<tr height="20"><td colspan="8" height="20" class="line2"'
                                     ' valign="bottom" nowrap><nobr>)([\w.,\-&\'\s]+)'
                                     '(</nobr></td></tr>)', row):
          self.agency = re_groups[1]
          
        # Check if the agent might be interested in picture books.
        if 'picture book' in row.lower():
          self.picture_books = True
          
  def ToDict(self):
    """Convert agent object into dictionary (great for csv.DictWriter)."""
    return {AGENT_NAME_KEY: self.agent_name,
            AGENT_ID_KEY: self.agent_id,
            AGENT_URL_KEY: self.agent_url,
            PICTURE_BOOK_KEY: self.picture_books,
            AGENCY_KEY: self.agency}
            
          
def GetAgentIdsFromCsv(path_to_dir):
  """Gets list of agent IDs from CSV.
  
  Args:
    path_to_dir: str, path to directory CSV resides in.
  """
  path_to_file = os.path.join(path_to_dir, AGENT_IDS_FILE_NAME)
  
  with open(path_to_file, 'r') as f:
    csv_reader = csv.DictReader(f)
    for row in csv_reader:
      yield row[AGENT_ID_KEY]
      

def WriteToCsv(agents):
  """Write agent objects to CSV.
  
  Args:
    agents: list of agent objects, agents to write to CSV.
  """
  # Convert agent objects into dictionaries.
  to_write = [agent.ToDict() for agent in agents]
  
  # Get an example agent object to compute output file name and header for CSV.
  example_agent = agents.pop()
  output_file_path = os.path.join(example_agent.path_to_dir, OUTPUT_FILE_NAME)
    
  # Write CSV.
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
