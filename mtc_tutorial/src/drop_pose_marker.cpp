#include <rclcpp/rclcpp.hpp>
#include <interactive_markers/interactive_marker_server.hpp>
#include <visualization_msgs/msg/interactive_marker.hpp>
#include <geometry_msgs/msg/pose.hpp>
#include <boost/bind.hpp>

using namespace boost::placeholders;

class DropPoseMarker {
public:
  DropPoseMarker() : node_{std::make_shared<rclcpp::Node>("drop_pose_marker")} {
    server_ = std::make_shared<interactive_markers::InteractiveMarkerServer>("drop_pose_marker", node_);
    makeMarker();
    pub_ = node_->create_publisher<geometry_msgs::msg::Pose>("/drop_pose", 10);
  }

  void makeMarker() {
    visualization_msgs::msg::InteractiveMarker int_marker;
    int_marker.header.frame_id = "panda_link0";
    int_marker.header.stamp = node_->now();
    int_marker.name = "drop_pose";
    int_marker.description = "Drop Position (drag to set)";
    int_marker.scale = 0.2;

    // Default pose (x=0.5, y=0.0, z=0.0)
    int_marker.pose.position.x = 0.5;
    int_marker.pose.position.y = 0.0;
    int_marker.pose.position.z = 0.0;
    int_marker.pose.orientation.w = 1.0;

    // Cube control
    visualization_msgs::msg::InteractiveMarkerControl control;
    control.always_visible = true;
    control.markers.push_back(createCubeMarker());
    int_marker.controls.push_back(control);

    // 6‑DOF controls (rotation + translation)
    std::vector<std::string> axes = {"x", "y", "z"};
    for (const auto& axis : axes) {
      geometry_msgs::msg::Quaternion quat;
      if (axis == "x") { quat.w = 1.0; quat.x = 1.0; quat.y = 0.0; quat.z = 0.0; }
      else if (axis == "y") { quat.w = 1.0; quat.x = 0.0; quat.y = 1.0; quat.z = 0.0; }
      else if (axis == "z") { quat.w = 1.0; quat.x = 0.0; quat.y = 0.0; quat.z = 1.0; }

      visualization_msgs::msg::InteractiveMarkerControl rot, mov;
      rot.orientation = quat;
      rot.name = "rotate_" + axis;
      rot.interaction_mode = visualization_msgs::msg::InteractiveMarkerControl::ROTATE_AXIS;
      mov.orientation = quat;
      mov.name = "move_" + axis;
      mov.interaction_mode = visualization_msgs::msg::InteractiveMarkerControl::MOVE_AXIS;
      int_marker.controls.push_back(rot);
      int_marker.controls.push_back(mov);
    }

    server_->insert(int_marker, boost::bind(&DropPoseMarker::processFeedback, this, _1));
    server_->applyChanges();
  }

  visualization_msgs::msg::Marker createCubeMarker() {
    visualization_msgs::msg::Marker marker;
    marker.type = visualization_msgs::msg::Marker::CUBE;
    marker.scale.x = 0.1;
    marker.scale.y = 0.1;
    marker.scale.z = 0.1;
    marker.color.r = 0.0;
    marker.color.g = 1.0;
    marker.color.b = 0.0;
    marker.color.a = 0.8;
    return marker;
  }

  void processFeedback(const visualization_msgs::msg::InteractiveMarkerFeedback::ConstSharedPtr& feedback) {
    if (feedback->event_type == visualization_msgs::msg::InteractiveMarkerFeedback::POSE_UPDATE) {
      pub_->publish(feedback->pose);
      RCLCPP_INFO(node_->get_logger(), "New drop pose: (%.3f, %.3f, %.3f)",
                  feedback->pose.position.x,
                  feedback->pose.position.y,
                  feedback->pose.position.z);
    }
  }

  rclcpp::Node::SharedPtr node_;
private:
  std::shared_ptr<interactive_markers::InteractiveMarkerServer> server_;
  rclcpp::Publisher<geometry_msgs::msg::Pose>::SharedPtr pub_;
};

int main(int argc, char** argv) {
  rclcpp::init(argc, argv);
  auto node = std::make_shared<rclcpp::Node>("drop_pose_marker");
  DropPoseMarker marker;
  rclcpp::spin(marker.node_);
  rclcpp::shutdown();
  return 0;
}
