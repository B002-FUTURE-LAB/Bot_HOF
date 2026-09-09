#!/usr/bin/env python3
"""Cancela todas as metas pendentes de /navigate_to_pose e confirma a resposta."""
import json
import sys

import rclpy
from nav2_msgs.action import NavigateToPose
from rclpy.action import ActionClient
from rclpy.node import Node


def main() -> int:
    rclpy.init()
    node = Node("future_lab_cancel_navigation")
    client = ActionClient(node, NavigateToPose, "/navigate_to_pose")
    try:
        if not client.wait_for_server(timeout_sec=8.0):
            print(json.dumps({"ok": False, "error": "Action /navigate_to_pose indisponível."}))
            return 3
        future = client.async_cancel_all_goals()
        rclpy.spin_until_future_complete(node, future, timeout_sec=10.0)
        response = future.result()
        if response is None:
            print(json.dumps({"ok": False, "error": "Sem resposta ao cancelamento."}))
            return 4
        print(json.dumps({"ok": True, "goals_canceling": len(response.goals_canceling)}))
        return 0
    finally:
        client.destroy()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    sys.exit(main())
