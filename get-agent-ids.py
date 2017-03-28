"""Tool for grabbing agent IDs and pages from publishers marketplace.

Query is typically just something like 'agent'.
"""

import os
import re
import sys
import time
import urllib

MEMBER_FILE_NAME = '%s.html'
MEMBER_URL = 'http://www.publishersmarketplace.com/members/%s/'
QUERY_FILE_NAME = '%s_%s.html'
QUERY_URL = 'http://www.publishersmarketplace.com/pm/search?ss_p=%s&ss_q=%s&ss_c=memberpage'
MAX_PAGES = 15

def DownloadQueryPages(query_string, path_to_dir):
  """Download query pages.
  
  Args:
    query_string: str, query string for searching.
    path_to_dir: str, path to directory to save files.
  """
  formatted_query_string = '+'.join(query_string.split())
  for page_index in range(1, MAX_PAGES + 1):
    url = QUERY_URL % (str(page_index), formatted_query_string)
    file_path = os.path.join(path_to_dir, QUERY_FILE_NAME % (formatted_query_string, page_index))
    time.sleep(1)
    urllib.urlretrieve(url, file_path)


def ExtractMemberIdsFromFiles(path_to_dir):
  """Extract member IDs from HTML files.
  
  Args:
    path_to_dir: str, path to directory to save files.
    
  Return:
    Member IDs.
  """
  member_ids = []
  
  results = os.popen('ls %s' % path_to_dir)
  file_names = [row.strip('\n') for row in results]
  
  for file_name in file_names:
    path = os.path.join(path_to_dir, file_name)
    with open(path, 'r') as f:
      for row in f:
        for re_groups in re.findall(r'(<a href="\/members\/)([\w]+)(\/">)', row):
          member_ids.append(re_groups[1])

  return member_ids
  
  
def IsAgent(member_id, path_to_dir):
  """Checks whether the member is an agent.
  
  Args:
    member_id: str, member ID.
    path_to_dir: str, path to directory to save files.
    
  Returns:
    Boolean.
  """
  url = MEMBER_URL % member_id
  file_path = os.path.join(path_to_dir, MEMBER_FILE_NAME % member_id)
  time.sleep(1)
  urllib.urlretrieve(url, file_path)
  
  with open(file_path, 'r') as f:
    for row in f:
      if re.search(r'agent : <a href="mailto:', row):
        return True
    
  return False
  
  
def main():
  if len(sys.argv) != 4:
    print 'usage: python get-member-ids.py "query string" /path/to/dir download?'
    
  query_string = sys.argv[1]
  path_to_dir = sys.argv[2]
  download = True if sys.argv[3] == 'True' else False
  
  if download:
    DownloadQueryPages(query_string, path_to_dir)
    
  agent_ids = [member_id for member_id in ExtractMemberIdsFromFiles(path_to_dir)
               if IsAgent(member_id, path_to_dir)]
  
  for agent_id in agent_ids:
    print agent_id
    

if __name__ == '__main__':
  main()
  
