# from https://stackoverflow.com/questions/47063311/using-jq-to-count
def count(s):
    reduce s as $_ (0;.+1);

def count(stream; cond):
    count(stream | cond // empty);

# useful links
# playground https://jqplay.org/
# cheatsheet https://gist.github.com/olih/f7437fb6962fb3ee9fe95bda8d2c8fa4

# useful jq

# keys for an object in an array
# jq '.data.entry[0] | keys' file

# count items in array
# jq 'reduce .data.entry[] as $_ (0;.+1)' file

# first 10 items in array
# jq '.data.entry[:10]' file
