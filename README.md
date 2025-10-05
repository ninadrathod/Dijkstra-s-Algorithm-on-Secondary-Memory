# Dijkstra-s-Algorithm-on-Secondary-Memory

## 1. Input File Requirements

### 1.1 `nodes.txt` - Node Definitions 📍

This file must contain the definition and coordinates for every node in the graph. Each line must follow the format below:

```
<node_id> <x_coordinate> <y_coordinate>
```
### 1.2 `edges.txt` - Edge Definitions 🔗

This file defines the connections (edges) and their associated weights between the nodes. Each line must follow the format below:

```
<start_node_id> <end_node_id> <edge_weight>
```

### Data Integrity Note (Crucial) ⚠️

All `<start_node_id>` and `<end_node_id>` values specified in the `edges.txt` file **MUST** refer to `<node_id>` entries that are already present in the `nodes.txt` file.
Failing to ensure node ID pre-existence will result in data parsing errors or invalid graph construction.
