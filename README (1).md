# Mini Social Network App
### Discrete Structures & Theory — Chapter 8 Integration Project

---

## Overview

A Python implementation of a mini social network that applies core discrete mathematics concepts including **set theory**, **relations**, and **graph algorithms** to model real-world social interactions.

---

## Features

| Feature | Description |
|---|---|
| Add / Remove Users | Manage user registry using a **set** |
| Follow / Unfollow | Directed relation between users |
| Friend / Unfriend | Symmetric (mutual) relation |
| Mutual Friends | Set intersection on friend sets |
| Groups | Set-based group membership |
| BFS Recommendations | Friend-of-friend discovery via Breadth-First Search |
| Dijkstra Path | Weighted shortest connection path between users |

---

## Theoretical Ties to Course Chapters

### Sets (Chapter 2 — Set Theory)
- `self.users` is a Python `set` — each user is a unique element
- Groups are stored as `dict[str, set]` — membership is a set relation
- Mutual friends use **set intersection** (`A ∩ B`)
- Common groups use **set intersection** across group membership sets

```python
# Example: mutual friends = set intersection
mutual = self.friends["Alice"] & self.friends["Dave"]
# → {'Bob', 'Carol'}
```

### Relations (Chapter 3 — Relations & Functions)
- **Follow** is a *directed*, *non-symmetric* binary relation: `(follower, followee) ∈ follows`
- **Friendship** is a *symmetric* relation: if `(A, B) ∈ friends` then `(B, A) ∈ friends`
- Both are represented as adjacency dictionaries of sets

```python
# Directed relation (follow)
follows["Alice"] = {"Bob", "Carol"}

# Symmetric relation (friend) — both sides maintained
friends["Alice"] = {"Bob"}
friends["Bob"]   = {"Alice"}
```

### Graphs (Chapter 6 — Graph Theory)
- The social network is modeled as a **weighted undirected graph** (for friends)
- Edge weight between two users = `1 / (mutual_friends + 1)`
  - Stronger connections (more mutual friends) → lower weight → preferred path

```
Alice ── Bob ── Dave ── Eve
  \              /
   Carol────────
```

### BFS — Breadth-First Search (Chapter 7)
- Used for **friend-of-friend recommendations**
- Explores all users within `depth` hops from the source
- Filters out existing friends and self

```
BFS from Alice (depth=2):
  Level 1: Bob, Carol  (direct friends — excluded)
  Level 2: Dave        (recommended ✓)
```

### Dijkstra's Algorithm (Chapter 7)
- Used to find the **strongest connection path** between two users
- Priority queue (min-heap) selects the lowest-weight next hop
- Smaller weights = more mutual friends = stronger social bond

```
Alice → Eve shortest path:
Alice → Bob → Dave → Eve  (weight: 3.0)
```

---

## Project Structure

```
mini_social_network.py    ← Main implementation
README.md                 ← This file
```

---

## How to Run

```bash
python mini_social_network.py
```

No external dependencies — uses only Python standard library (`collections`, `heapq`).

---

## Class: `SocialNetwork`

### User Management
| Method | Description |
|---|---|
| `add_user(username)` | Register a new user |
| `remove_user(username)` | Delete user and clean all relations |
| `display_user_info(username)` | Print friends, following, groups |

### Follow Relations (Directed)
| Method | Description |
|---|---|
| `follow(follower, followee)` | Add directed follow relation |
| `unfollow(follower, followee)` | Remove follow relation |

### Friend Relations (Symmetric)
| Method | Description |
|---|---|
| `add_friend(user1, user2)` | Add mutual friendship |
| `remove_friend(user1, user2)` | Remove mutual friendship |
| `list_mutual_friends(user1, user2)` | Return set intersection of friend sets |

### Groups (Set Operations)
| Method | Description |
|---|---|
| `create_group(name)` | Initialize a new group (empty set) |
| `join_group(user, group)` | Add user to group set |
| `leave_group(user, group)` | Remove user from group set |
| `group_members(group)` | Return the set of members |
| `common_groups(user1, user2)` | Return groups both users share |

### Graph Algorithms
| Method | Description |
|---|---|
| `bfs_recommendations(user, depth)` | BFS friend-of-friend suggestions |
| `dijkstra_connection_path(src, tgt)` | Weighted shortest path via Dijkstra |

---

## Sample Output

```
── Mutual Friends ──
Mutual friends of Alice & Dave: {'Carol', 'Bob'}

── BFS Recommendations for Alice ──
Recommended users: ['Dave']

── Dijkstra: Alice → Eve ──
Shortest path: Alice → Bob → Dave → Eve, weight: 3.0
```

---

## Design Decisions

- **Sets over lists** for O(1) membership checks and natural set operations
- **Directed adjacency dict** for follows, **bidirectional** for friends — matching mathematical definitions
- **Weighted edges** in Dijkstra reflect social closeness, not just hop count
- All methods return descriptive strings for easy UI integration

---

## Reflection

This project demonstrates how abstract mathematical structures directly map to real-world software:

- **Set theory** → membership, intersection, difference in social graphs
- **Relations** → asymmetric (follow) vs symmetric (friend) social ties
- **Graph algorithms** → efficient discovery and traversal of social connections
- **BFS** → level-order exploration mirrors how social circles expand
- **Dijkstra** → weighted optimization reflects real connection strength

These theoretical foundations are not just academic — they underpin production systems like LinkedIn's "People You May Know" and Twitter's follow graph.
