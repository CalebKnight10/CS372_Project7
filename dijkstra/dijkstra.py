# Caleb Knight
# Project 7
# Routing with Dijkstra


import sys
import json
import math  # If you want to use math.inf for infinity


def ipv4_to_value(ipv4_addr):
    """
    Convert a dots-and-numbers IP address to a single numeric value.

    Example:

    There is only one return value, but it is shown here in 3 bases.

    ipv4_addr: "255.255.0.0"
    return:    0xffff0000 0b11111111111111110000000000000000 4294901760

    ipv4_addr: "1.2.3.4"
    return:    0x01020304 0b00000001000000100000001100000100 16909060
    """

    # First use split to get individual nums
    ip_bytes = ipv4_addr.split('.')

    # Need to loop through nums to make ints
    decimal = 0 
    for b in range(len(ip_bytes)):
        ints = int(b)
        # Build nums by shifting hex nums ex: (0xc6 << 24) | ....
        ip_bytes[b] = int(ip_bytes[b]) << (24-(b*8))
        decimal += ip_bytes[b]
    return decimal

def get_subnet_mask_value(slash):
    """
    Given a subnet mask in slash notation, return the value of the mask
    as a single number. The input can contain an IP address optionally,
    but that part should be discarded.

    Example:

    There is only one return value, but it is shown here in 3 bases.

    slash:  "/16"
    return: 0xffff0000 0b11111111111111110000000000000000 4294901760

    slash:  "10.20.30.40/23"
    return: 0xfffffe00 0b11111111111111111111111000000000 4294966784
    """

    # Check if it is in ipv4 format, if so get just the subnet
    if '.' in slash:
        subnet_mask = slash.split('/')
        subnet_mask = subnet_mask[1]

    # If not, just get the subnet number
    else:
        subnet_mask = slash.split('/')
        subnet_mask = subnet_mask[1]
    
    subnet_mask = int(subnet_mask)
    subnet_val = 0

    for x in range(32):
        if x < int(slash.split('/')[1]): 
            subnet_val = (subnet_val << 1) + 1
        else:
            subnet_val = (subnet_val << 1)

    return subnet_val

def ips_same_subnet(ip1, ip2, slash):
    """
    Given two dots-and-numbers IP addresses and a subnet mask in slash
    notataion, return true if the two IP addresses are on the same
    subnet.

    FOR FULL CREDIT: this must use your get_subnet_mask_value() and
    ipv4_to_value() functions. Don't do it with pure string
    manipulation.

    This needs to work with any subnet from /1 to /31

    Example:

    ip1:    "10.23.121.17"
    ip2:    "10.23.121.225"
    slash:  "/23"
    return: True
    
    ip1:    "10.23.230.22"
    ip2:    "10.24.121.225"
    slash:  "/16"
    return: False
    """

    # Get the address from ipv4
    ip1_addr = ipv4_to_value(ip1)
    ip2_addr = ipv4_to_value(ip2)

    # Get subnet too
    subnet_mask = get_subnet_mask_value(slash)

    # Make networks ints and use bitwise addr & subnet
    ip1_network = (ip1_addr & subnet_mask)
    ip2_network = (ip2_addr & subnet_mask)

    # Compare
    if ip1_network == ip2_network:
        return True

    else: 
        return False
        
def find_router_for_ip(routers, ip):
    """
    Search a dictionary of routers (keyed by router IP) to find which
    router belongs to the same subnet as the given IP.

    Return None if no routers is on the same subnet as the given IP.

    FOR FULL CREDIT: you must do this by calling your ips_same_subnet()
    function.

    Example:

    [Note there will be more data in the routers dictionary than is
    shown here--it can be ignored for this function.]

    routers: {
        "1.2.3.1": {
            "netmask": "/24"
        },
        "1.2.4.1": {
            "netmask": "/24"
        }
    }
    ip: "1.2.3.5"
    return: "1.2.3.1"


    routers: {
        "1.2.3.1": {
            "netmask": "/24"
        },
        "1.2.4.1": {
            "netmask": "/24"
        }
    }
    ip: "1.2.5.6"
    return: None
    """

    # Go through the routers and get the netmask num
    for addr in routers:
        netmask = routers[addr]["netmask"]

        # Check if the ips are on the same subnet based off of the netmask
        # that we got previously
        if ips_same_subnet(addr, ip, netmask):
            return addr
    return None    



def dijkstras_shortest_path(routers, src_ip, dest_ip):
    """
    This function takes a dictionary representing the network, a source
    IP, and a destination IP, and returns a list with all the routers
    along the shortest path.

    The source and destination IPs are **not** included in this path.

    Note that the source IP and destination IP will probably not be
    routers! They will be on the same subnet as the router. You'll have
    to search the routers to find the one on the same subnet as the
    source IP. Same for the destination IP. [Hint: make use of your
    find_router_for_ip() function from the last project!]

    The dictionary keys are router IPs, and the values are dictionaries
    with a bunch of information, including the routers that are directly
    connected to the key.

    This partial example shows that router `10.31.98.1` is connected to
    three other routers: `10.34.166.1`, `10.34.194.1`, and `10.34.46.1`:

    {
        "10.34.98.1": {
            "connections": {
                "10.34.166.1": {
                    "netmask": "/24",
                    "interface": "en0",
                    "ad": 70
                },
                "10.34.194.1": {
                    "netmask": "/24",
                    "interface": "en1",
                    "ad": 93
                },
                "10.34.46.1": {
                    "netmask": "/24",
                    "interface": "en2",
                    "ad": 64
                }
            },
            "netmask": "/24",
            "if_count": 3,
            "if_prefix": "en"
        },
        ...

    The "ad" (Administrative Distance) field is the edge weight for that
    connection.

    **Strong recommendation**: make functions to do subtasks within this
    function. Having it all built as a single wall of code is a recipe
    for madness.
    """

    to_visit = [] # List of all needs need to vist
    distance = {} # For any given node, it will hold distance from itself to start node
    parent = {} # List key of node that leads back to the start along shortest path

    for n in nodes:
        parent{n} = None
        distance{n} = math.inf
        to_visit += n 

    while to_visit is not []:
        # Find node in to_visit that is the smallest distance -> curr_node
        # Remove curr_node from to_visit
        # For each of curr_node's neighbors in to_visit:
            # Compute dist from start to neighbor (This is dist of curr_node + weight of neighbor)
            # If the comp dist is less than the neighbors curr value in distance:
                # Set neighbor val in distance to comp dist
                # Set neighbors parent to curr_node

#------------------------------
# DO NOT MODIFY BELOW THIS LINE
#------------------------------
def read_routers(file_name):
    with open(file_name) as fp:
        data = fp.read()

    return json.loads(data)

def find_routes(routers, src_dest_pairs):
    for src_ip, dest_ip in src_dest_pairs:
        path = dijkstras_shortest_path(routers, src_ip, dest_ip)
        print(f"{src_ip:>15s} -> {dest_ip:<15s}  {repr(path)}")

def usage():
    print("usage: dijkstra.py infile.json", file=sys.stderr)

def main(argv):
    try:
        router_file_name = argv[1]
    except:
        usage()
        return 1

    json_data = read_routers(router_file_name)

    routers = json_data["routers"]
    routes = json_data["src-dest"]

    find_routes(routers, routes)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
    
