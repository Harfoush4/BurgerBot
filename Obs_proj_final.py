import rclpy
import math

from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf2_ros import TransformRegistration
from rclpy.qos import QoSProfile, ReliabilityPolicy

#Creating the Speed and dirction memberships so i can calculate them after the rules are fired
speeds={'low':[0.01,0.05,0.1],'med':[0.1,0.15,0.2],'high':[0.2,0.21,0.22]}
directions={'left':[-0.3,-0.2,-0.1],'straight':[-0.1,0,0.1],'right':[0.1,0.2,0.3]}

#Creating a class to have different sensors as objects to make it easier to add more sensors
class sensor:
    def __init__(self,input):
        #This is the input membership function:
        self.distance_fuzz={'near':[0, 0.6, 0.65], 'med':[0.6, 0.65, 0.7], 'far':[0.65, 0.7, 1]}
        #Mebership values:
        self.mv_near=0
        self.mv_far=0
        self.mv_med=0
        self.input=input


    #creating a trainglular function to calculate the values in the Falling edge and the rising edge
    def triangle(self,m1,input):
        #So if the input corrsepond to a point after the highest point in my membership it calculates falling edge:
        if input>=m1[1] and input<=m1[2]:
            return (m1[2]-input)/(m1[2]-m1[1]) #Falling edge Equation
        #and if the input corresponds to a point before the highest point it calculates the rising edge:
        elif input>=m1[0] and input<=m1[1]:
            return (input-m1[0])/(m1[1]-m1[0]) #rising edge equation


    #now calculating the membership values according to the input
    #So here 1 input goes in which is the reading of the sensor and 3 membership values are returned
    def fuzzification(self):
        if self.input>=self.distance_fuzz['near'][0] and self.input<self.distance_fuzz['med'][0]:
            self.distance_fuzz = 'near'
            self.mv_near=1
            self.mv_med = 0
            self.mv_far = 0
            return self.mv_near , self.mv_med, self.mv_far
        elif self.input>=self.distance_fuzz['near'][2] and self.input<self.distance_fuzz['far'][0]:
            self.distance_fuzz = 'med'
            self.mv_near = 0
            self.mv_med = 1
            self.mv_far = 0
            return self.mv_near, self.mv_med, self.mv_far

        elif self.input>self.distance_fuzz['med'][2]:
            self.distance_fuzz= 'far'
            self.mv_near = 0
            self.mv_med = 0
            self.mv_far = 1
            return self.mv_near, self.mv_med, self.mv_far
        elif self.input>=self.distance_fuzz['med'][0]and self.input<=self.distance_fuzz['near'][2]:

            self.mv_near=self.triangle(self.distance_fuzz['near'], self.input)
            self.mv_med=self.triangle(self.distance_fuzz['med'], self.input)
            self.mv_far = 0
            return self.mv_near, self.mv_med, self.mv_far
        elif self.input>=self.distance_fuzz['far'][0]and self.input<=self.distance_fuzz['med'][2]:
            self.mv_near=0
            self.mv_med=self.triangle(self.distance_fuzz['med'], self.input)
            self.mv_far=self.triangle(self.distance_fuzz['far'], self.input)
            return self.mv_near, self.mv_med, self.mv_far

def defuzzification(fsr, fs, fsl):
    firing = []
    for i in (fsr):
        for j in (fs):
            for k in (fsl):
                firing.append(min(i, j, k))
    return firing


def Defuzz(firing_list):
    global speeds
    global directions
    sum_speed = 0
    sum_direction = 0
    p = 0

    # rule1 Near/Near/Near
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule2 Near/Near/Med
    speed = speeds.get('low')[1]
    direction = directions.get('right')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule3 Near/Near/Far
    speed = speeds.get('low')[1]
    direction = directions.get('right')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule4 Near/Med/Near
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule5 Near/Med/Med
    speed = speeds.get('low')[1]
    direction = directions.get('right')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule6 Near/Med/Far
    speed = speeds.get('low')[1]
    direction = directions.get('right')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule7 Near/Far/Near
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule8 Near/Far/Med
    speed = speeds.get('low')[1]
    direction = directions.get('right')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule9 Near/Far/Far
    speed = speeds.get('low')[1]
    direction = directions.get('right')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule10 Med/Near/Near
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule11 Med/Near/Med
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule12 Med/Near/Far
    speed = speeds.get('low')[1]
    direction = directions.get('right')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule13 Med/Med/Near
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule14 Med/Med/Med
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule15 Med/Med/Far
    speed = speeds.get('low')[1]
    direction = directions.get('right')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule16 Med/Far/Near
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule17 Med/Far/Med
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule18 Med/Far/Far
    speed = speeds.get('low')[1]
    direction = directions.get('right')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule19 Far/Near/Near
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule20 Far/Near/Med
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule21 Far/Near/Far
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule22 Far/Med/Near
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule23 Far/Med/Med
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule24 Far/Med/Far
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule25 Far/Far/Near
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule26 Far/Far/Med
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule27 Far/Far/Far
    speed = speeds.get('low')[1]
    direction = directions.get('straight')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    speed = sum_speed / sum(firing_list)
    direction = sum_direction / sum(firing_list)
    return speed, direction



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
    if (twstmsg_ != None):
        pub_.publish(twstmsg_)


def clbk_laser(msg):
    global regions_, twstmsg_

    regions_ = {
        # LIDAR readings are anti-clockwise
        'front1': find_nearest(msg.ranges[0:5]),
        'front2': find_nearest(msg.ranges[355:360]),
        'frontL': find_nearest(msg.ranges[5:15]),
        'frontR': find_nearest(msg.ranges[345:355]),
        'right': find_nearest(msg.ranges[265:275]),
        'fright': find_nearest(msg.ranges[310:320]),
        'fleft': find_nearest(msg.ranges[40:50]),
        'left': find_nearest(msg.ranges[85:95])

    }
    twstmsg_ = movement()


# Find nearest point
def find_nearest(list):
    f_list = filter(lambda item: item > 0.0, list)  # exclude zeros
    return min(min(f_list, default=10), 10)


# Basic movement method
def movement():
    # print("here")
    global regions_, mynode_
    regions = regions_

    print("Min distance in front region: ", regions_['front1'], regions_['front2'])

    # create an object of twist class, used to express the linear and angular velocity of the turtlebot
    msg = Twist()
    x = min(regions_['front1'], regions_['front2'])
    x2 = regions_['frontR']
    x3 = regions_['frontL']
    fs = sensor(x).fuzzification()
    fsr = sensor(x2).fuzzification()
    fsl = sensor(x3).fuzzification()
    print("These are the membership values", fs, fsr, fsl)
    firing = defuzzification(fsl, fs, fsr)
    print("The firing strength", defuzzification(fsl, fs, fsr))
    s, d = Defuzz(firing)
    print(f"speed:{s},direction:{d}")

    msg.linear.x = s
    msg.angular.z = d * -1
    return msg

# used to stop the rosbot
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





