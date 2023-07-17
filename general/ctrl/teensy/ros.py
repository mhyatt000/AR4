""" KDL or MoveIt """


#!/usr/bin/env python

import rospy
import moveit_commander
import moveit_msgs.msg

def robot_control():
    # Initialize the move_group API
    moveit_commander.roscpp_initialize(sys.argv)

    # Initialize the rospy node
    rospy.init_node('robot_control', anonymous=True)
    
    # This interface to MoveIt is called a MoveGroupCommander
    # It is the primary way users interact with a planning group.
    group_name = "manipulator" # change this to your robot's planning group name
    move_group = moveit_commander.MoveGroupCommander(group_name)
    
    # You can get the name of the reference frame for this robot
    planning_frame = move_group.get_planning_frame()
    print("============ Planning frame: %s" % planning_frame)
    
    # Set a goal joint value
    joint_goal = move_group.get_current_joint_values()
    joint_goal[0] = 0  # First joint
    joint_goal[1] = 0  # Second joint
    joint_goal[2] = 0  # Third joint
    joint_goal[3] = 0  # Fourth joint
    joint_goal[4] = 0  # Fifth joint
    joint_goal[5] = 0  # Sixth joint

    # Send the goal to move the robot
    move_group.go(joint_goal, wait=True)
    
    # Stop the robot after reaching the goal
    move_group.stop()
    
    # Shut down MoveIt cleanly
    moveit_commander.roscpp_shutdown()

    # End the rospy node
    rospy.spin()

if __name__ == '__main__':
    try:
        robot_control()
    except rospy.ROSInterruptException:
        pass


from PyKDL import *

# Define a chain
chain = Chain()
joint1 = Joint(Joint.TransZ)
frame1 = Frame(Vector(0.0, 0.0, 1.0))
segment1 = Segment(joint1, frame1)
chain.addSegment(segment1)

joint2 = Joint(Joint.TransZ)
frame2 = Frame(Vector(1.0, 0.0, 0.0))
segment2 = Segment(joint2, frame2)
chain.addSegment(segment2)

# Initialize a solver
fk_solver = ChainFkSolverPos_recursive(chain)

# Define joint angles
joint_angles = JntArray(2)
joint_angles[0] = 0.5
joint_angles[1] = 0.5

# Calculate forward kinematics
end_effector_pose = Frame()
fk_solver.JntToCart(joint_angles, end_effector_pose)

print(end_effector_pose)


"""
Please note that you would need to define the chain to match your specific robotic manipulator.
Each segment in the chain represents a link in your robot, and the frame associated with the
segment defines the transformation from one joint to the next.

As mentioned, Python's PyKDL currently does not provide a way to solve inverse kinematics. For
inverse kinematics, you would typically use the `ChainIkSolverPos_NR` or `ChainIkSolverPos_NR_JL`
classes, but these are not available in PyKDL.

If you really want to compute inverse kinematics in Python, one workaround would be to use a
numerical method for inverse kinematics, such as those available in libraries like SciPy. However,
these methods may not be as efficient or accurate as the ones provided by KDL. Another option would
be to use a different library that includes Python bindings for inverse kinematics, such as IKPy.
If using C++ is an option, you could use KDL's C++ library, which includes these functionalities.

The limitations of PyKDL might change in the future if the library is updated to include more
features from the C++ version. So it's worth keeping an eye on the development of PyKDL.
"""
