import rclpy
import math

from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf2_ros import TransformRegistration
from rclpy.qos import QoSProfile, ReliabilityPolicy

speeds = {'low': [0.01, 0.05, 0.1], 'med': [0.1, 0.15, 0.2], 'high': [0.2, 0.25, 0.3]}
directions = {'left': [-0.3, -0.2, -0.1], 'straight': [-0.1, 0, 0.1], 'right': [0.1, 0.2, 0.3]}

class sensor:
    def __init__(self, input):
        self.distance_fuzz = {'near': [0, 0.6, 0.65], 'med': [0.6, 0.65, 0.7], 'far': [0.65, 0.7, 1]}
        self.mv_near = 0
        self.mv_far = 0
        self.mv_med = 0
        self.input = input
        # self.rbs={'near':[0,0.6,0.65], 'med':[0.6,0.65,0.7],'far':[0.65,0.7,1]}

    def triangle(self, m1, input):
        # print(input,"dah el da5lni")
        if input >= m1[1] and input <= m1[2]:
            # print((m1[2]-input)/(m1[2]-m1[1]),"rising")
            return (m1[2] - input) / (m1[2] - m1[1])
        elif input >= m1[0] and input <= m1[1]:
            # print((input-m1[0])/(m1[1]-m1[0]),"falling")
            return (input - m1[0]) / (m1[1] - m1[0])

    def fuzzification(self):
        if self.input >0.9:
            self.input=0.9

        if self.input >= self.distance_fuzz['near'][0] and self.input < self.distance_fuzz['med'][0]:
            self.distance_fuzz = 'near'
            self.mv_near = 1
            self.mv_med = 0
            self.mv_far = 0
            return self.mv_near, self.mv_med, self.mv_far
        if self.input >= self.distance_fuzz['near'][2] and self.input < self.distance_fuzz['far'][0]:
            self.distance_fuzz = 'med'
            self.mv_near = 0
            self.mv_med = 1
            self.mv_far = 0
            return self.mv_near, self.mv_med, self.mv_far

        if self.input > self.distance_fuzz['med'][2] :
            self.distance_fuzz = 'far'
            self.mv_near = 0
            self.mv_med = 0
            self.mv_far = 1
            return self.mv_near, self.mv_med, self.mv_far
        elif self.input >= self.distance_fuzz['med'][0] and self.input <= self.distance_fuzz['near'][2]:

            self.mv_near = self.triangle(self.distance_fuzz['near'], self.input)
            self.mv_med = self.triangle(self.distance_fuzz['med'], self.input)
            self.mv_far = 0
            return self.mv_near, self.mv_med, self.mv_far
        elif self.input >= self.distance_fuzz['far'][0] and self.input <= self.distance_fuzz['med'][2]:
            self.mv_near = 0
            self.mv_med = self.triangle(self.distance_fuzz['med'], self.input)
            self.mv_far = self.triangle(self.distance_fuzz['far'], self.input)
            return self.mv_near, self.mv_med, self.mv_far


def fire_strength_front(fsr, fs, fsl):
    firing = []
    for i in (fsr):
        for j in (fs):
            for k in (fsl):
                firing.append(min(i, j, k))
    return firing

def fire_strenght_right(rfs,rbs):

    firing=[]
    for i in (rfs):
        print("i is ",i)
        for j in (rbs):
            firing.append(min(i,j))
    print("here i am",firing)
    return firing


def Defuzz_front(firing_list):
    global speeds
    global directions
    sum_speed = 0
    sum_direction = 0
    p = 0
    # rule1
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule2
    speed = speeds.get('low')[1]
    direction = directions.get('right')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule3
    speed = speeds.get('low')[1]
    direction = directions.get('right')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule4
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule5
    speed = speeds.get('low')[1]
    direction = directions.get('right')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule6
    speed = speeds.get('low')[1]
    direction = directions.get('right')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule7
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule8
    speed = speeds.get('low')[1]
    direction = directions.get('right')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule9
    speed = speeds.get('low')[1]
    direction = directions.get('right')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule10
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule11
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule12
    speed = speeds.get('low')[1]
    direction = directions.get('right')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule13
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule14
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule15
    speed = speeds.get('low')[1]
    direction = directions.get('right')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule16
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule17
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule18
    speed = speeds.get('low')[1]
    direction = directions.get('right')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule19
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule20
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule21
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule22
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule23
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule24
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule25
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule26
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    # rule27
    speed = speeds.get('low')[1]
    direction = directions.get('straight')[1]
    sum_speed += firing_list[p] * speed
    sum_direction += firing_list[p] * direction
    p += 1

    speed = sum_speed / sum(firing_list)
    direction = sum_direction / sum(firing_list)
    return speed, direction


def Defuzz_right(fs):
    global speeds
    global directions
    sum_speed=0
    sum_direction=0
    #rule1
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += fs[0] * speed
    sum_direction += fs[0] * direction
    #rule2
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += fs[1] * speed
    sum_direction += fs[1] * direction
    #rule3
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += fs[2] * speed
    sum_direction += fs[2] * direction
    #rule4
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += fs[3] * speed
    sum_direction += fs[3] * direction
    #rule5
    speed = speeds.get('med')[1]
    direction = directions.get('straight')[1]
    sum_speed += fs[4] * speed
    sum_direction += fs[4] * direction
    #rule6
    speed = speeds.get('med')[1]
    direction = directions.get('left')[1]
    sum_speed += fs[5] * speed
    sum_direction += fs[5] * direction
    #rule7
    speed = speeds.get('med')[1]
    direction = directions.get('right')[1]
    sum_speed += fs[6] * speed
    sum_direction += fs[6] * direction
    #rule8
    speed = speeds.get('med')[1]
    direction = directions.get('right')[1]
    sum_speed += fs[7] * speed
    sum_direction += fs[7] * direction
    #rule9
    speed = speeds.get('med')[1]
    direction = directions.get('right')[1]
    sum_speed += fs[8] * speed
    sum_direction += fs[8] * direction

    speed=sum_speed/sum(fs)
    direction=sum_direction/sum(fs)
    return speed,direction

#x = float(input('Enter right front sensor value:'))
#x2 = float(input('Enter right back sensor value:'))
#x3 = float(input('Enter left front sensor value:'))



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
        'frontL': find_nearest(msg.ranges[5:22]),
        'frontR': find_nearest(msg.ranges[338:355]),
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



    # create an object of twist class, used to express the linear and angular velocity of the turtlebot
    msg = Twist()
    if (min(regions_['front1'], regions_['front2'],regions_['frontL'],regions_['frontR'])<1):
        print("Min distance in front region: ", regions_['front1'], regions_['front2'])
        print("----------OBS_____AVD------------")
        x = min(regions_['front1'], regions_['front2'])
        x2 = regions_['frontR']
        x3 = regions_['frontL']
        fs = sensor(x).fuzzification()
        fsr = sensor(x2).fuzzification()
        fsl = sensor(x3).fuzzification()
        print("These are the membership values", fs, fsr, fsl)
        firing = fire_strength_front(fsl, fs, fsr)
        print("The firing strength", fire_strength_front(fsl, fs, fsr))
        s, d = Defuzz_front(firing)
        print(f"speed:{s},direction:{d}")

        msg.linear.x = s
        msg.angular.z = d * -1
        return msg
    # elif min(regions_['right'], regions_['fright']>1):
    #     print("fixing........................................fixing")
    #     msg.linear.x = 0.1
    #     msg.angular.z = -0.2
    #     return msg

    else:
        print("----------Right_____Edge------------")
        x = regions_['fright']
        x2 = regions_['right']
        rfs = sensor(x).fuzzification()
        rbs = sensor(x2).fuzzification()
        print("These are the membership values", rfs, rbs)
        firing = fire_strenght_right(rfs, rbs)
        print("The firing strength", fire_strenght_right(rfs, rbs))
        s, d = Defuzz_right(firing)
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





