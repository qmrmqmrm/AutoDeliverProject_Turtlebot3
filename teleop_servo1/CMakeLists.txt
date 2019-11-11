cmake_minimum_required(VERSION 2.8.3)
project(teleop_servo1)

add_compile_options(-std=c++11)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  geometry_msgs
  std_msgs
  message_generation
)



set(CMAKE_CXX_FLAGS "-L/usr/local/lib -pthread")


add_message_files(
  FILES
  TriggerMsg.msg
 )

generate_messages(
   DEPENDENCIES
   std_msgs
 )


catkin_package(
  INCLUDE_DIRS
  LIBRARIES teleop_servo1
  CATKIN_DEPENDS roscpp std_msgs geometry_msgs
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

add_executable(servo_pub /home/turtle/catkin_ws/src/teleop_servo1/src/servo_pub.cpp)
target_link_libraries(servo_pub ${catkin_LIBRARIES})
add_dependencies(servo_pub ${mode_second}_EXPORTED_TARGETS ${catkin_EXPORTED_TARGETS})

add_executable(signal_pub /home/turtle/catkin_ws/src/teleop_servo1/src/signal_pub.cpp)
target_link_libraries(signal_pub ${catkin_LIBRARIES})
add_dependencies(signal_pub ${mode_second}_EXPORTED_TARGETS ${catkin_EXPORTED_TARGETS})


add_executable(trigger_pub /home/turtle/catkin_ws/src/teleop_servo1/src/trigger_pub.cpp)
target_link_libraries(trigger_pub ${catkin_LIBRARIES})
add_dependencies(trigger_pub ${mode_second}_EXPORTED_TARGETS ${catkin_EXPORTED_TARGETS})
