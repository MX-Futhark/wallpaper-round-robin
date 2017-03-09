# Wallpaper Round Robin

Generates wallpapers for multiple monitors setups by combining png or jpg images together.

## Requirements

- Python 3
- PIL

## Usage

This section aims at guiding the user by providing basic examples. 
For more details, please run `python3 main.py -h`.

There are three generation methods which work as follow.

Let the setup contain two monitors, and suppose we have the following file tree:

```
dirI
|____A.png
|____B.png

dirII
|____1.png
|____2.jpg
|____3.jpg
```

### Round Robin method

Run the following command:

`python3 main.py -i dirI dirII --m round_robin`

The resulting wallpapers should be generated according to the following pattern, 
in this order:

```
+---+---+    +---+---+    +---+---+    +---+---+    +---+---+    +---+---+
| A | 1 |    | B | 1 |    | B | 2 |    | A | 2 |    | A | 3 |    | B | 3 |
+---+---+    +---+---+    +---+---+    +---+---+    +---+---+    +---+---+

+---+---+    +---+---+    +---+---+    +---+---+    +---+---+    +---+---+
| B | 1 |    | A | 1 |    | A | 2 |    | B | 2 |    | B | 3 |    | A | 3 |
+---+---+    +---+---+    +---+---+    +---+---+    +---+---+    +---+---+ 
```

### One-to-one method

Run the following command:

`python3 main.py -i dirI dirII --m one_to_one`

The resulting wallpapers should be generated according to the following pattern, 
in this order:

```
+---+---+    +---+---+    +---+---+    +---+---+    +---+---+    +---+---+
| A | 1 |    | B | 2 |    | A | 3 |    | B | 1 |    | A | 2 |    | B | 3 |
+---+---+    +---+---+    +---+---+    +---+---+    +---+---+    +---+---+
```

### Gallery method

Run the following command (note that `-i` takes only one directory):

`python3 main.py -i dirII --m gallery`

The resulting wallpapers should be generated according to the following pattern, 
in this order:

```
+---+---+    +---+---+    +---+---+
| A | B |    | B | C |    | C | A |
+---+---+    +---+---+    +---+---+
```
