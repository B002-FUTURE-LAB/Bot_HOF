#!/usr/bin/env python3
"""Envia uma meta Nav2 única e devolve JSON com o resultado mensurável."""
import argparse
import json
import math
import sys
import time

import rclpy
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose
from rclpy.action import ActionClient
from rclpy.node import Node


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--x", type=float, required=True)
    parser.add_argument("--y", type=float, required=True)
    parser.add_argument("--yaw", type=float, required=True)
    parser.add_argument("--timeout", type=float, default=70.0)
    args = parser.parse_args()
    if not all(math.isfinite(value) for value in (args.x, args.y, args.yaw, args.timeout)):
        print(json.dumps({"ok": False, "error": "Parâmetros não finitos."}))
        return 2

    rclpy.init()
    node = Node("future_lab_navigate_once")
    client = ActionClient(node, NavigateToPose, "/navigate_to_pose")
    try:
        if not client.wait_for_server(timeout_sec=8.0):
            print(json.dumps({"ok": False, "error": "Action /navigate_to_pose indisponível."}))
            return 3
        goal = NavigateToPose.Goal()
        goal.pose = PoseStamped()
        goal.pose.header.frame_id = "map"
        goal.pose.header.stamp = node.get_clock().now().to_msg()
        goal.pose.pose.position.x = args.x
        goal.pose.pose.position.y = args.y
        goal.pose.pose.orientation.z = math.sin(args.yaw / 2.0)
        goal.pose.pose.orientation.w = math.cos(args.yaw / 2.0)
        sent = client.send_goal_async(goal)
        rclpy.spin_until_future_complete(node, sent, timeout_sec=10.0)
        handle = sent.result()
        if handle is None or not handle.accepted:
            print(json.dumps({"ok": False, "error": "Meta Nav2 rejeitada."}))
            return 4
        result = handle.get_result_async()
        rclpy.spin_until_future_complete(node, result, timeout_sec=args.timeout)
        response = result.result()
        if response is None:
            handle.cancel_goal_async()
            print(json.dumps({"ok": False, "error": "Timeout aguardando meta Nav2; cancelamento solicitado."}))
            return 5
        status = int(response.status)
        print(json.dumps({"ok": status == 4, "status": status, "x": args.x, "y": args.y, "yaw": args.yaw}))
        return 0 if status == 4 else 6
    finally:
        client.destroy()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    sys.exit(main())
