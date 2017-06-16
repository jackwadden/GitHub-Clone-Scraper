import requests, json, os.path

# File Format where the first line is totals
# Counts: <#> Uniques: <#>
# <count> <timestamp> <uniques>
# <count> <timestamp> <uniques>

# BE CAREFUL; PLAINTEXT CREDENTIALS!
username = "username"
password = "password"
repos = ['VASim', 'ANMLZoo', 'Automata-to-Routing']

# Class defining the clone information returned by GitHub about each repo
class CloneRecord:
    def __init__(self, count, timestamp, uniques):
        self.count = count
        self.timestamp = timestamp
        self.uniques = uniques


# Parses a file line into a CloneRecord object
def parseFileRecord(record):
    entries = record.split()
    result = CloneRecord(entries[0], entries[1], entries[2])
    return result

# Reads clone file into list of records in dictionary
def readCloneFile(fn, recordMap):

    # open file, if it doesn't exist, create it
    if os.path.isfile(fn):
        f = open(fn, 'r')
    else:
        f = open(fn, 'w+')
        writeTotalsLine(f,0,0)
        f.seek(0)

    # skip first line (contains totals)
    parseTotals(f.readline())

    # read entries
    for line in f:
        # parse line entry into object
        record = parseFileRecord(line)
        # map timestamp strings to record objects
        recordMap[record.timestamp] = record

# Writes the first line of every file given a count and uniques total
def writeTotalsLine(f, count, uniques):
    line = "Counts: " + str(count) + " Uniques: " + str(uniques) + "\n"
    f.write(line)

# Writes the file given a record map. Automatically counts clone/unique totals
def writeCloneFile(fn, recordMap):

    f = open(fn, 'w')

    # get totals
    countTotal = 0
    uniquesTotal = 0
    for timestamp, record in recordMap.items():
        countTotal += record.count
        uniquesTotal += record.uniques

    # write totals
    writeTotalsLine(f, countTotal, uniquesTotal)

    # write entries
    for timestamp, record in recordMap.items():
        line = str(record.count) + " " + str(record.timestamp) + " " + str(record.uniques) + "\n"
        f.write(line)

# Retrieves clone info from GitHub as a .json object
def getCloneCounts():
    url = "https://api.github.com/repos/" + username + "/" + repo + "/traffic/clones"
    response = requests.get(url, auth=(username,password))
    return response.json()

# Pretty prints a record
def printRecord(record):
    line = str(record.count) + " " + str(record.timestamp) + " " + str(record.uniques)
    print line

# Parses first line in file. Returns tuple of totals
def parseTotals(line):
    print line
    entries = line.split()
    return entries[1],entries[3]

#
def updateRepo(repo):
    # Init recordMap
    recordMap = dict()

    # Choose filename
    fn = repo + ".txt"

    # Read configuration file for repo
    print "Reading from old file..."
    readCloneFile(fn, recordMap)

    for timestamp, record in recordMap.items():
        printRecord(record)
        print "---------------------"

    # Get data from Github
    print "Asking Github for data..."
    counts = getCloneCounts()
    print counts
    print "---------------------"

    # Build clone map
    print "Building data structure from GitHub data..."
    entries = counts["clones"]
    for entry in entries:
        ts = entry["timestamp"]
        print entry["count"], ts, entry["uniques"]
        recordMap[ts] = CloneRecord(entry["count"], ts, entry["uniques"])

    print "---------------------"

    # Write clone map to file
    print "Writing data structure back to file..."
    writeCloneFile(fn, recordMap)

    print "---------------------"
    print "DONE"

#####################################################

for repo in repos:
    updateRepo(repo)
