execute_process(COMMAND "/home/monojit/simulation_ws/build/vrx-master/vrx_gazebo/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/monojit/simulation_ws/build/vrx-master/vrx_gazebo/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
