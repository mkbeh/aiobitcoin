Network
-------

* **clear_banned()**
    **Parameters:** - absent

    **Returns:** None

    **Return type:** NoneType

* **get_peer_info(to_list=True)**
    **Parameters:**

    * **to_list** (bool) - Will return list or genexpr

    **Returns:** Returns data about each connected network node as a json array of objects.

    **Return type:** list or genexpr

* **get_network_info()**
    **Parameters:** - absent

    **Returns:** Returns an object containing various state info regarding P2P networking.

    **Return type:** dict

* **list_banned(to_list=True)**
    **Parameters:**

    * **to_list** (bool) - Will return list or genexpr

    **Returns:** List all banned IPs/Subnets.

    **Return type:** list or genexpr

* **ping()**
    *Requests that a ping be sent to all other nodes, to measure ping time.
    Results provided in getpeerinfo, pingtime and pingwait fields are decimal seconds.
    Ping command is handled in queue with all other commands, so it measures processing backlog, not just
    network ping.*

    **Parameters:** - absent

    **Returns:** None

    **Return type:** NoneType

* **set_ban(subnet, command='add', bantime=0, absolute=False)**
    *Attempts to add or remove an IP/Subnet from the banned list.*

    **Parameters:**

    * **subnet** (str) - The IP/Subnet (see getpeerinfo for nodes IP) with an optional netmask (default is /32 = single IP)
    * **command** (str) - 'add' to add an IP/Subnet to the list, 'remove' to remove an IP/Subnet from the list
    * **bantime** (int) - Time in seconds how long (or until when if [absolute] is set) the IP is banned (0 or empty means using the default time of 24h which can also be overwritten by the -bantime startup argument)
    * **absolute** (bool) - If set, the bantime must be an absolute timestamp in seconds since epoch (Jan 1 1970 GMT)

    **Returns:** None

    **Return type:** NoneType

    **Raises:** aiobitcoin.bitcoinerrors.InvalidIpOrSubnet -
    if IP or subnet is incorrect