# A-Pathfinder-Algorithm-Visualizer

Algorithm visualizer for search-based path planning algorithms: DFS, BFS, A*. Built with pygame.

## Setup

```sh
python -m venv env_name
source env_name/bin/activate
pip install -r requirements.txt
```

## Usage
For Search Algorithms:
- run `python search.py`
- select a node for start node
- select a node for end node
- draw obstacles
- click space to confirm the map
- press 1 to run DFS, press 2 to run BFS, press 3 to run A*

For Sample Algorithms:
- run `python sample.py`
- click anywhere to select starting node
- click anywhere to select end node
- click and drag anywhere to draw obstacles
- click space to confirm the map
- press 1 to run RRT, press 2 to run RRT*
