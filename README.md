# 🤖 MoveIt 2 Pick-and-Place with Custom GUI – Complete Tutorial

This repository provides a complete, working pick-and-place solution using MoveIt Task Constructor (MTC) on the Panda robot, controlled by a custom Python GUI.

## Contents
- ataullah_ra/ (formerly mtc_tutorial) — C++ MTC node: pick-and-place logic, GUI topic integration
- mtc_gui/ — Python Tkinter GUI: drop pose control, object tracking, start/stop/repeat

## System Overview
- Environment: ROS 2 (Jazzy), MoveIt 2 built from source
- Robot: Franka Emika Panda (simulated with fake controllers)
- User Interface: Custom Tkinter GUI communicating with the MTC node via ROS 2 topics
- Workflow: user sets a drop pose (X, Y, Z, absolute world coordinates in the panda_link0 frame) in the GUI, then presses Start. The MTC node plans and executes a full pick-and-place sequence.

## Quick Start

Terminal 1 — environment:
    source ~/ws_moveit/install/setup.bash
    ros2 launch moveit2_tutorials mtc_demo.launch.py

Terminal 2 — GUI:
    source ~/ws_moveit/install/setup.bash
    ros2 run mtc_gui mtc_gui

Terminal 3 — MTC node:
    source ~/ws_moveit/install/setup.bash
    ros2 launch ataullah_ra pick_place_demo.launch.py

In the GUI, set a drop pose and click Start.

## Notes on Drop Pose
The drop pose is specified in the panda_link0 (world) frame. Keep target positions
within the Panda's reachable workspace (roughly within 0.85m of the base) to avoid
"no IK found" planning failures.

## Troubleshooting
- Package not found: source ~/ws_moveit/install/setup.bash in every terminal.
- Robot doesn't move / planning fails: check drop pose is within reachable range.
- IK errors: verify the IK frame configuration in the place stage matches the target pose frame.
- Gripper action server errors: ensure panda_hand_controller is loaded by the environment launch file.

License: Apache 2.0 (as used in MoveIt)
