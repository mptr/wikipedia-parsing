from subprocess import Popen, PIPE, STDOUT
import re, time

def revokeLn():
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    print(CURSOR_UP_ONE + ERASE_LINE)

# run a commend on cli
def cmdline(command):
    process = Popen(args=command,stdout=PIPE,shell=True)
    return process.communicate()[0]

# restarts the container if exited
def restartContainer(name):
    exitedRegex = re.compile(r'(Exited|Up).*?' + name, re.M)
    out = cmdline("docker ps -a").decode("utf-8")
    m = exitedRegex.search(out)
    if(m == None): # unknown
        print("cant determine docker status", out)
        exit()
        return
    elif(m.group().startswith("Up")): return # is running
    print("restarting docker container")
    out = cmdline("docker start " + name).decode("utf-8") # issue restart
    time.sleep(10) # wait for the server to start up
    revokeLn()
    print("restarted docker container: " + out)


# start batch# is 1
batch = 1

# finds last occourence of wikidump-xxx...xxx.ttl.gz
lastOkRegex = re.compile(r'wikidump-(\d{9,})\.ttl\.gz(?![\s\S]*wikidump-\d{9,}\.ttl\.gz)', re.M) # re.m = Multiline

while(batch < 9789):
    restartContainer("wikibase") # restart docker if necessary
    # out = cmdline("bash scripts/sample.sh").decode("utf-8") # run the load script
    print("running import of batch stating at " + str(batch))
    out = cmdline("docker exec -it wikibase bash -c \"/wdqs/loadData.sh -n wdq -s " + str(batch) + " -d /munge/mungeOut | tee -a log.txt\"").decode("utf-8") # run the load script
    m = lastOkRegex.search(out) # analyze output
    if(m == None): exit("Couldnt determine last process number in:\n" + out)
    nrStr = m.groups()[0]
    newBatch = int(nrStr) # get last processed batch number
    if(newBatch < batch):
        print("ERROR: new batch detected was lt old", batch, newBatch)
        break
    batch = newBatch
    revokeLn()
    print("resuming job at batch" + str(batch))

