
import rclpy
import math

from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf2_ros import TransformRegistration
from rclpy.qos import QoSProfile, ReliabilityPolicy


mynode_ = None
pub_ = None
regions_ = {
    'right': 0,
    'fright': 0,
    'front1': 0,
    'front2': 0,
    'fleft': 0,
    'left': 0,
}
twstmsg_ = None

# main function attached to timer callback
def timer_callback():
    global pub_, twstmsg_
    if ( twstmsg_ != None ):
        pub_.publish(twstmsg_)


def clbk_laser(msg):
    global regions_, twstmsg_
    
    regions_ = {
        #LIDAR readings are anti-clockwise
        'front1':  find_nearest (msg.ranges[0:5]),
        'front2':  find_nearest (msg.ranges[355:360]),
        'right':  find_nearest(msg.ranges[250:280]),
        'fright': find_nearest (msg.ranges[290:340]),
        'fleft':  find_nearest (msg.ranges[40:50]),
        'left':   find_nearest (msg.ranges[85:95])
        
    }    
    twstmsg_= movement()

    
# Find nearest point
def find_nearest(list):
    f_list = filter(lambda item: item > 0.0, list)  # exclude zeros
    return min(min(f_list, default=10), 10)

#Basic movement method
def movement():
    global regions_, mynode_
    regions = regions_
    desired_distance=0.37 #this is how far i want the robot to be from the right edge

    # The Following values are the gains that will be multiplied to the error
    kp=0.5 #this is the gain for the proportinal error
    ki=0.000001 #this is tha gain for the integrial error
    kd=0.1#this is the gain for the diffrential error

    e=0 #this is the proportional error
    eprev=0 #variables to store the errors
    ei=0
    ed=0
    e=desired_distance-regions_['fright'] #Calculating the error which is the differnce between the desired and the sensor reading

    ei=e+ei #calculating the integral error which takes into considration all previous errors
    ed=e-eprev #calculating the diffrantial error which is the diffrence between the current and previous
    eprev=e
    #The equation of The PID controller:
    direction=kp*e+ki*ei+kd*ed
    print("Min distance in right region: ", regions_['right'],regions_['fright'])
    
    #create an object of twist class, used to express the linear and angular velocity of the turtlebot 
    msg = Twist()

    #The PID value is going to be my angular velocity and my Linear velocity is going to be constant med speed     
    msg.linear.x = 0.15
    msg.angular.z = direction
    return msg

#used to stop the rosbot
def stop():
    global pub_
    msg = Twist()
    msg.angular.z = 0.0
    msg.linear.x = 0.0
    pub_.publish(msg)


def main():
    global pub_, mynode_

    rclpy.init()
    mynode_ = rclpy.create_node('reading_laser')

    # define qos profile (the subscriber default 'reliability' is not compatible with robot publisher 'best effort')
    qos = QoSProfile(
        depth=10,
        reliability=ReliabilityPolicy.BEST_EFFORT,
    )

    # publisher for twist velocity messages (default qos depth 10)
    pub_ = mynode_.create_publisher(Twist, '/cmd_vel', 10)

    # subscribe to laser topic (with our qos)
    sub = mynode_.create_subscription(LaserScan, '/scan', clbk_laser, qos)

    # Configure timer
    timer_period = 0.2  # seconds 
    timer = mynode_.create_timer(timer_period, timer_callback)

    # Run and handle keyboard interrupt (ctrl-c)
    try:
        rclpy.spin(mynode_)
    except KeyboardInterrupt:
        stop()  # stop the robot
    except:
        stop()  # stop the robot
    finally:
        # Clean up
        mynode_.destroy_timer(timer)
        mynode_.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
