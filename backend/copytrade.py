followers = {}

def follow(master, follower):

    if master not in followers:
        followers[master] = []

    followers[master].append(follower)

def broadcast_trade(master, trade):

    copied = []

    for f in followers.get(master, []):

        copied.append({
            "follower": f,
            "trade": trade
        })

    return copied