cmake_minimum_required(VERSION 2.8.3)
project(teleop_servo1)

 add_compile_options(-std=c++11)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  geometry_msgs
  std_msgs
  message_generation
)

add_message_files(
 FILES
 mode_msg.msg
)

generate_messages(
   DEPENDENCIES
   std_msgs
)

catkin_package(
  #INCLUDE_DIRS include
  LIBRARIES teleop_servo1
  CATKIN_DEPENDS roscpp std_msgs geometry_msgs
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

add_executable(mode_select src/mode_select.cpp)
target_link_libraries(mode_select ${catkin_LIBRARIES})
add_dependencies(mode_select ${${catkin_LIBRARIES}}_EXPORTED_TARGETS ${catkin_EXPORTED_TARGETS})

add_executable(servo_pub src/servo_pub.cpp)
target_link_libraries(servo_pub ${catkin_LIBRARIES})
add_dependencies(servo_pub ${${catkin_LIBRARIES}}_EXPORTED_TARGETS ${catkin_EXPORTED_TARGETS})

add_executable(step_pub src/step_pub.cpp)
target_link_libraries(step_pub ${catkin_LIBRARIES})
add_dependencies(step_pub ${${catkin_LIBRARIES}}_EXPORTED_TARGETS ${catkin_EXPORTED_TARGETS})
