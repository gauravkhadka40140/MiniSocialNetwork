"""
Mini Social Network App
=======================
Uses sets for groups, relation pairs for friendships/follows,
and graph algorithms (BFS/Dijkstra) for recommendations.

Theoretical Ties:
- Sets        → Group membership (Set Theory, Chapter 2)
- Relations   → Follow/friend pairs (Relations & Functions, Chapter 3)
- Graphs      → Social graph for recommendations (Graph Theory, Chapter 6)
- BFS         → Shortest path / friend-of-friend discovery (Graph Algorithms, Chapter 7)
- Dijkstra    → Weighted recommendation paths (Chapter 7)
"""

from collections import defaultdict, deque
import heapq


# ─────────────────────────────────────────────
#  Data Structures
# ─────────────────────────────────────────────

class SocialNetwork:
    def __init__(self):
        # Set of all users
        self.users: set = set()

        # Groups: dict[group_name] → set of usernames
        self.groups: dict[str, set] = defaultdict(set)

        # Follows: directed relation — follows[u] = set of users u follows
        self.follows: dict[str, set] = defaultdict(set)

        # Friends: symmetric relation — friends[u] = set of u's friends
        self.friends: dict[str, set] = defaultdict(set)

    # ──────────────────────────────────────────
    #  User Management
    # ──────────────────────────────────────────

    def add_user(self, username: str) -> str:
        """Register a new user."""
        if username in self.users:
            return f"User '{username}' already exists."
        self.users.add(username)
        return f"User '{username}' added successfully."

    def remove_user(self, username: str) -> str:
        """Remove a user and clean up all relations."""
        if username not in self.users:
            return f"User '{username}' not found."
        self.users.discard(username)
        # Clean follows
        self.follows.pop(username, None)
        for u in self.follows:
            self.follows[u].discard(username)
        # Clean friends
        for friend in list(self.friends.get(username, [])):
            self.friends[friend].discard(username)
        self.friends.pop(username, None)
        # Clean groups
        for group in self.groups.values():
            group.discard(username)
        return f"User '{username}' removed."

    # ──────────────────────────────────────────
    #  Follow / Unfollow (Directed Relation)
    # ──────────────────────────────────────────

    def follow(self, follower: str, followee: str) -> str:
        """follower starts following followee."""
        if follower not in self.users or followee not in self.users:
            return "One or both users not found."
        if follower == followee:
            return "A user cannot follow themselves."
        self.follows[follower].add(followee)
        return f"'{follower}' now follows '{followee}'."

    def unfollow(self, follower: str, followee: str) -> str:
        """follower unfollows followee."""
        if followee not in self.follows.get(follower, set()):
            return f"'{follower}' is not following '{followee}'."
        self.follows[follower].discard(followee)
        return f"'{follower}' unfollowed '{followee}'."

    # ──────────────────────────────────────────
    #  Friend / Unfriend (Symmetric Relation)
    # ──────────────────────────────────────────

    def add_friend(self, user1: str, user2: str) -> str:
        """Create a mutual friendship (symmetric relation)."""
        if user1 not in self.users or user2 not in self.users:
            return "One or both users not found."
        if user1 == user2:
            return "A user cannot befriend themselves."
        self.friends[user1].add(user2)
        self.friends[user2].add(user1)
        return f"'{user1}' and '{user2}' are now friends."

    def remove_friend(self, user1: str, user2: str) -> str:
        """Remove mutual friendship."""
        self.friends[user1].discard(user2)
        self.friends[user2].discard(user1)
        return f"'{user1}' and '{user2}' are no longer friends."

    def list_mutual_friends(self, user1: str, user2: str) -> set:
        """Return the set intersection of both users' friend sets."""
        return self.friends.get(user1, set()) & self.friends.get(user2, set())

    # ──────────────────────────────────────────
    #  Groups (Set Operations)
    # ──────────────────────────────────────────

    def create_group(self, group_name: str) -> str:
        if group_name in self.groups:
            return f"Group '{group_name}' already exists."
        self.groups[group_name]  # initializes empty set via defaultdict
        return f"Group '{group_name}' created."

    def join_group(self, username: str, group_name: str) -> str:
        if username not in self.users:
            return f"User '{username}' not found."
        self.groups[group_name].add(username)
        return f"'{username}' joined group '{group_name}'."

    def leave_group(self, username: str, group_name: str) -> str:
        self.groups[group_name].discard(username)
        return f"'{username}' left group '{group_name}'."

    def group_members(self, group_name: str) -> set:
        return self.groups.get(group_name, set())

    def common_groups(self, user1: str, user2: str) -> set:
        """Groups both users belong to (set intersection)."""
        u1_groups = {g for g, members in self.groups.items() if user1 in members}
        u2_groups = {g for g, members in self.groups.items() if user2 in members}
        return u1_groups & u2_groups

    # ──────────────────────────────────────────
    #  Graph Algorithms for Recommendations
    # ──────────────────────────────────────────

    def bfs_recommendations(self, username: str, depth: int = 2) -> list[str]:
        """
        BFS-based friend-of-friend recommendations.
        Returns users within `depth` hops who are not already friends/self.
        """
        if username not in self.users:
            return []

        visited = {username}
        queue = deque([(username, 0)])
        recommendations = []

        while queue:
            current, level = queue.popleft()
            if level >= depth:
                continue
            for neighbor in self.friends.get(current, set()):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, level + 1))
                    if neighbor not in self.friends.get(username, set()):
                        recommendations.append((neighbor, level + 1))

        return [r[0] for r in sorted(recommendations, key=lambda x: x[1])]

    def dijkstra_connection_path(self, source: str, target: str) -> tuple[list[str], float]:
        """
        Dijkstra's algorithm to find shortest weighted path between two users.
        Edge weight = 1 / (mutual friends + 1) — stronger connections weigh less.
        Returns (path, total_weight).
        """
        if source not in self.users or target not in self.users:
            return [], float('inf')

        dist = {source: 0.0}
        prev = {}
        pq = [(0.0, source)]

        while pq:
            cost, u = heapq.heappop(pq)
            if u == target:
                break
            if cost > dist.get(u, float('inf')):
                continue
            for v in self.friends.get(u, set()):
                mutual = len(self.list_mutual_friends(u, v))
                weight = 1.0 / (mutual + 1)
                new_cost = cost + weight
                if new_cost < dist.get(v, float('inf')):
                    dist[v] = new_cost
                    prev[v] = u
                    heapq.heappush(pq, (new_cost, v))

        # Reconstruct path
        if target not in dist:
            return [], float('inf')
        path = []
        node = target
        while node != source:
            path.append(node)
            node = prev.get(node)
            if node is None:
                return [], float('inf')
        path.append(source)
        path.reverse()
        return path, round(dist[target], 4)

    # ──────────────────────────────────────────
    #  Display Helpers
    # ──────────────────────────────────────────

    def display_user_info(self, username: str):
        if username not in self.users:
            print(f"User '{username}' not found.")
            return
        print(f"\n── {username} ──")
        print(f"  Friends  : {self.friends.get(username, set()) or 'None'}")
        print(f"  Following: {self.follows.get(username, set()) or 'None'}")
        groups = [g for g, m in self.groups.items() if username in m]
        print(f"  Groups   : {groups or 'None'}")

    def display_all_users(self):
        print(f"\nAll Users ({len(self.users)}): {self.users}")


# ─────────────────────────────────────────────
#  Demo / Main
# ─────────────────────────────────────────────

if __name__ == "__main__":
    net = SocialNetwork()

    print("=" * 50)
    print("       Mini Social Network Demo")
    print("=" * 50)

    # Add users
    for user in ["Alice", "Bob", "Carol", "Dave", "Eve"]:
        print(net.add_user(user))

    print("\n── Follow Relations ──")
    print(net.follow("Alice", "Bob"))
    print(net.follow("Alice", "Carol"))
    print(net.follow("Bob", "Dave"))
    print(net.follow("Carol", "Eve"))

    print("\n── Friendships ──")
    print(net.add_friend("Alice", "Bob"))
    print(net.add_friend("Alice", "Carol"))
    print(net.add_friend("Bob", "Dave"))
    print(net.add_friend("Carol", "Dave"))
    print(net.add_friend("Dave", "Eve"))

    print("\n── Groups ──")
    print(net.create_group("CS_Students"))
    print(net.create_group("Gamers"))
    for u in ["Alice", "Bob", "Carol"]:
        print(net.join_group(u, "CS_Students"))
    for u in ["Bob", "Dave", "Eve"]:
        print(net.join_group(u, "Gamers"))

    print("\n── Mutual Friends ──")
    mutual = net.list_mutual_friends("Alice", "Dave")
    print(f"Mutual friends of Alice & Dave: {mutual}")

    print("\n── Common Groups ──")
    common = net.common_groups("Alice", "Bob")
    print(f"Common groups of Alice & Bob: {common}")

    print("\n── BFS Recommendations for Alice ──")
    recs = net.bfs_recommendations("Alice", depth=2)
    print(f"Recommended users: {recs}")

    print("\n── Dijkstra: Alice → Eve ──")
    path, weight = net.dijkstra_connection_path("Alice", "Eve")
    print(f"Shortest path: {' → '.join(path)}, weight: {weight}")

    print("\n── User Profiles ──")
    for user in ["Alice", "Bob", "Dave"]:
        net.display_user_info(user)

    print("\n── Unfollow Demo ──")
    print(net.unfollow("Alice", "Bob"))

    print("\n── Remove Friend Demo ──")
    print(net.remove_friend("Alice", "Bob"))
    net.display_user_info("Alice")
