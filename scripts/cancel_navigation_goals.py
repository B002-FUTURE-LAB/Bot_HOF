#!/usr/bin/env python3
"""Cancela todas as metas pendentes de /navigate_to_pose e confirma a resposta."""
import json
import sys

import rclpy
from action_msgs.srv import CancelGoal
from rclpy.node import Node


def main() -> int:
    rclpy.init()
    node = Node("future_lab_cancel_navigation")
    # rclpy.ActionClient não expõe uma API pública para cancelar todas as
    # metas. A tentativa anterior usava async_cancel_all_goals(), método que
    # não existe e deixava a meta antiga executando. O protocolo ROS 2 define
    # este serviço para cada action; GoalInfo vazio significa "todas as
    # metas" e a resposta informa quantas foram efetivamente canceladas.
    client = node.create_client(CancelGoal, "/navigate_to_pose/_action/cancel_goal")
    try:
        if not client.wait_for_service(timeout_sec=8.0):
            print(json.dumps({"ok": False, "error": "Serviço de cancelamento do /navigate_to_pose indisponível."}))
            return 3
        future = client.call_async(CancelGoal.Request())
        rclpy.spin_until_future_complete(node, future, timeout_sec=10.0)
        response = future.result()
        if response is None:
            print(json.dumps({"ok": False, "error": "Sem resposta ao cancelamento."}))
            return 4
        print(json.dumps({"ok": True, "goals_canceling": len(response.goals_canceling)}))
        return 0
    finally:
        node.destroy_client(client)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    sys.exit(main())
