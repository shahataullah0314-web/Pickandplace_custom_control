cmake_minimum_required(VERSION 3.8)
project(ataullah_ra)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(moveit_task_constructor_core REQUIRED)
find_package(moveit_ros_planning_interface REQUIRED)
find_package(moveit_visual_tools REQUIRED)
find_package(interactive_markers REQUIRED)

add_executable(mtc_node src/mtc_node.cpp)
target_include_directories(mtc_node PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include/${PROJECT_NAME}>)
target_compile_features(mtc_node PUBLIC c_std_99 cxx_std_17)
ament_target_dependencies(mtc_node
  rclcpp
  moveit_task_constructor_core
  moveit_ros_planning_interface
  moveit_visual_tools)

add_executable(drop_pose_marker src/drop_pose_marker.cpp)
ament_target_dependencies(drop_pose_marker
  rclcpp
  interactive_markers)

install(TARGETS mtc_node drop_pose_marker
  DESTINATION lib/${PROJECT_NAME})

install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME})

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
