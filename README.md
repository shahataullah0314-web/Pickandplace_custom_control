# 🤖 My MoveIt 2 Pick-and-Place Project (with a Custom GUI)

This is a project I built to control a Franka Emika Panda robot arm using MoveIt Task Constructor (MTC), with my own Tkinter GUI on top so I could set a drop location by hand and just hit Start.

It didn't work on the first try. Or the fifth. This README is as much a record of what actually went wrong and how I found it as it is a setup guide — I wanted to write it the way I wish someone had written it for me.

## What's in here
- `ataullah_ra/` — the C++ MTC node. This is the brain: it plans and executes the actual pick-and-place motion.
- `mtc_gui/` — my Python Tkinter GUI. Lets me track the object's position, set a drop pose, and start/stop/repeat the task.

## How it works
I set a drop pose (X, Y, Z in the robot's world frame) in the GUI and press Start. The node plans a full sequence — open hand, move to pick, approach, grasp, lift, move to place, place, retreat, return home — and executes it on the real controllers.

## Running it

Terminal 1 — environment:
    source ~/ws_moveit/install/setup.bash
    ros2 launch moveit2_tutorials mtc_demo.launch.py

Terminal 2 — GUI:
    source ~/ws_moveit/install/setup.bash
    ros2 run mtc_gui mtc_gui

Terminal 3 — MTC node:
    source ~/ws_moveit/install/setup.bash
    ros2 launch ataullah_ra pick_place_demo.launch.py

## The problems I actually ran into (and how I solved them)

### 1. The arm just... wouldn't move
This was the most frustrating part. I'd click Start, the terminal would fill up with planning logs, everything *looked* like it was working, and then — nothing. No error I could immediately understand, no arm motion, silence.

I stopped guessing and started checking things one at a time instead of assuming. I checked `/joint_states` before and after clicking Start and compared the numbers. They were identical, down to the decimal. That told me the robot genuinely never moved — it wasn't a visualization issue or a delay, execution simply wasn't happening.

### 2. Chasing the wrong error at first
Early on I assumed it was a controller problem, since the arm wasn't moving. I checked `ros2 control list_controllers` — everything was active. I checked the action servers — they existed and were connected. That ruled out the "obvious" explanation, which was honestly a little deflating, but it meant I had to keep digging instead of settling for a quick fix that wouldn't have actually fixed anything.

### 3. Finding the real error meant getting the logs right
I kept trying to read the MTC node's terminal output, but I kept losing it — Ctrl+C too early, wrong process killed, wrong package name typed. I eventually just piped everything to a log file with `tee` and made myself wait through a full Start cycle before touching the terminal again. That patience is what finally surfaced the actual line I needed:

    place pose IK (0/1120): no IK found

Once I saw that, the picture became clear. Out of over a thousand candidate poses, the robot's arm could not find a single valid configuration to reach the one I'd asked for. It wasn't broken. It just genuinely couldn't get there.

### 4. Understanding *why* it couldn't reach
This is the part that actually taught me something. My drop pose wasn't in world coordinates — it was relative to the object's frame. So when I typed in a value I thought was "a small offset," it was actually being added on top of wherever the object happened to be, and could easily push the target outside the arm's real reach (about 0.85m from the base) or into an orientation with no valid solution.

The default value in the original code happened to land somewhere reachable. My custom values didn't. That's why it worked when I left it alone and failed the moment I touched it — not a bug in the traditional sense, just coordinates I didn't fully understand yet.

### 5. The fix
I changed the place pose's reference frame from the object's frame to the robot's world frame (`panda_link0`). Now when I type X, Y, Z into the GUI, it means exactly what I think it means — an absolute position in the robot's workspace. I also picked a saner default drop location, mirroring where the object is picked up from.

I kept it simple on purpose: `setIKFrame` stayed pointed at the object, since that defines *what* gets placed at the pose; only `header.frame_id` needed to change, since that defines *what coordinate system the pose is written in*. Separating those two ideas in my head is what made the fix click.

## What I'd tell past-me
- If the robot doesn't move, check `/joint_states` before assuming anything about planning or controllers.
- Don't trust that "no errors scrolled by" means it worked — actually read the final status line.
- Log to a file. Terminal scrollback lies to you when you Ctrl+C at the wrong moment.
- If a pose-based failure only happens with *some* values and not others, the frame it's expressed in is the first thing to check, not the last.

## Other issues I hit along the way
- **Package not found** — forgot to source `~/ws_moveit/install/setup.bash` in a fresh terminal. Every terminal needs it.
- **Gripper action server not connecting** — the hand controller wasn't loaded; needed to confirm the environment launch file actually starts it.
- **`no IK found` on the grasp side too, briefly** — same root cause as the place pose, different stage.

## Notes on drop pose
Keep target positions within roughly 0.85m of the robot base. Outside that, you'll likely see the same `no IK found` failure I did.

License: Apache 2.0 (as used in MoveIt)

— Ataullah
