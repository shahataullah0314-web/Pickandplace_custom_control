#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose, PoseStamped
from std_msgs.msg import String
import threading

class MTCGui:
    def __init__(self, root):
        self.root = root
        self.root.title("MTC Control Panel")
        self.root.geometry("500x400")

        # ROS node
        rclpy.init(args=None)
        self.node = rclpy.create_node('mtc_gui')
        self.drop_pub = self.node.create_publisher(Pose, '/drop_pose', 10)
        self.cmd_pub = self.node.create_publisher(String, '/mtc_command', 10)
        self.object_pose_sub = self.node.create_subscription(PoseStamped, '/object_pose', self.object_callback, 10)

        # Variables
        self.object_x = tk.StringVar(value="0.0")
        self.object_y = tk.StringVar(value="0.0")
        self.object_z = tk.StringVar(value="0.0")
        self.drop_x = tk.StringVar(value="0.5")
        self.drop_y = tk.StringVar(value="0.0")
        self.drop_z = tk.StringVar(value="0.0")

        self.build_gui()

        # ROS spinner thread
        self.spin_thread = threading.Thread(target=self.spin_ros)
        self.spin_thread.daemon = True
        self.spin_thread.start()

    def build_gui(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True)

        # Tab 1: Object Tracking
        track_frame = ttk.Frame(notebook)
        notebook.add(track_frame, text="Object Tracking")
        ttk.Label(track_frame, text="Object Pose (from planning scene):").pack(pady=5)
        ttk.Label(track_frame, text="X:").pack()
        self.x_label = ttk.Label(track_frame, textvariable=self.object_x)
        self.x_label.pack()
        ttk.Label(track_frame, text="Y:").pack()
        self.y_label = ttk.Label(track_frame, textvariable=self.object_y)
        self.y_label.pack()
        ttk.Label(track_frame, text="Z:").pack()
        self.z_label = ttk.Label(track_frame, textvariable=self.object_z)
        self.z_label.pack()

        # Tab 2: Drop Location
        drop_frame = ttk.Frame(notebook)
        notebook.add(drop_frame, text="Drop Location")
        ttk.Label(drop_frame, text="Set Drop Pose (relative to object):").pack(pady=5)
        ttk.Label(drop_frame, text="X:").pack()
        ttk.Entry(drop_frame, textvariable=self.drop_x).pack()
        ttk.Label(drop_frame, text="Y:").pack()
        ttk.Entry(drop_frame, textvariable=self.drop_y).pack()
        ttk.Label(drop_frame, text="Z:").pack()
        ttk.Entry(drop_frame, textvariable=self.drop_z).pack()
        ttk.Button(drop_frame, text="Apply Drop Pose", command=self.publish_drop).pack(pady=10)

        # Tab 3: Control
        ctrl_frame = ttk.Frame(notebook)
        notebook.add(ctrl_frame, text="Control")
        ttk.Button(ctrl_frame, text="▶ Start", command=self.start_task, width=15).pack(pady=5)
        ttk.Button(ctrl_frame, text="⏹ Stop", command=self.stop_task, width=15).pack(pady=5)
        ttk.Button(ctrl_frame, text="🔁 Repeat", command=self.repeat_task, width=15).pack(pady=5)

    def publish_drop(self):
        pose = Pose()
        pose.position.x = float(self.drop_x.get())
        pose.position.y = float(self.drop_y.get())
        pose.position.z = float(self.drop_z.get())
        pose.orientation.w = 1.0
        self.drop_pub.publish(pose)
        print(f"Drop pose set to ({pose.position.x}, {pose.position.y}, {pose.position.z})")

    def object_callback(self, msg):
        self.object_x.set(f"{msg.pose.position.x:.3f}")
        self.object_y.set(f"{msg.pose.position.y:.3f}")
        self.object_z.set(f"{msg.pose.position.z:.3f}")

    def start_task(self):
        cmd = String()
        cmd.data = "start"
        self.cmd_pub.publish(cmd)
        print("Sent Start command")

    def stop_task(self):
        cmd = String()
        cmd.data = "stop"
        self.cmd_pub.publish(cmd)
        print("Sent Stop command")

    def repeat_task(self):
        cmd = String()
        cmd.data = "repeat"
        self.cmd_pub.publish(cmd)
        print("Sent Repeat command")

    def spin_ros(self):
        rclpy.spin(self.node)

def main():
    root = tk.Tk()
    app = MTCGui(root)
    root.mainloop()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
