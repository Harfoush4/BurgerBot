
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



#Creating a function that takes the membership values and calulate the firing strength and append it to a list
def defuzzification(rfs,rbs):
    firing=[]
    for i in (rfs):
        print("i is ",i)
        for j in (rbs):
            firing.append(min(i,j))
    print("Firing list:",firing)
    return firing


#Next we take the firing list calculated above and multiple it with each rule of the rule base
#the rules has to be in the same order that is used in the 2 for loops above
def Defuzz(fs):
    global speeds
    global directions
    sum_speed=0
    sum_direction=0

    #rule1 Near/Near
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += fs[0] * speed
    sum_direction += fs[0] * direction

    #rule2 Near/Med
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += fs[1] * speed
    sum_direction += fs[1] * direction

    #rule3 Near/Far
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += fs[2] * speed
    sum_direction += fs[2] * direction

    #rule4 Med/Near
    speed = speeds.get('low')[1]
    direction = directions.get('left')[1]
    sum_speed += fs[3] * speed
    sum_direction += fs[3] * direction

    #rule5 Med/Med
    speed = speeds.get('med')[1]
    direction = directions.get('straight')[1]
    sum_speed += fs[4] * speed
    sum_direction += fs[4] * direction

    #rule6 Med/Far
    speed = speeds.get('med')[1]
    direction = directions.get('left')[1]
    sum_speed += fs[5] * speed
    sum_direction += fs[5] * direction

    #rule7 Far/Near
    speed = speeds.get('med')[1]
    direction = directions.get('right')[1]
    sum_speed += fs[6] * speed
    sum_direction += fs[6] * direction

    #rule8 Far/Med
    speed = speeds.get('high')[1]
    direction = directions.get('right')[1]
    sum_speed += fs[7] * speed
    sum_direction += fs[7] * direction

    #rule9 Far/Far
    speed = speeds.get('high')[1]
    direction = directions.get('right')[1]
    sum_speed += fs[8] * speed
    sum_direction += fs[8] * direction

    #dividing the summation of all the above rules by the sum of the firing list to get the final speed
    #same calculation for direction
    speed=sum_speed/sum(fs)
    direction=sum_direction/sum(fs)
    return speed,direction



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
        'right':  find_nearest(msg.ranges[265:275]),
        'fright': find_nearest (msg.ranges[310:320]),
        'fleft':  find_nearest (msg.ranges[40:50]),
        'left':   find_nearest (msg.ranges[85:95])

    }
    twstmsg_= movement()


# Find nearest point
def find_nearest(list):
    f_list = filter(lambda item: item > 0.0, list)  # exclude zeros
    return min(min(f_list, default=1), 1)

#Basic movement method
def movement():
    global regions_, mynode_
    regions = regions_

    print("Min distance in right region: ", regions_['right'],regions_['fright'])

    #create an object of twist class, used to express the linear and angular velocity of the turtlebot
    msg = Twist()
    #readings from both sensors
    fr=regions_['fright']
    r=regions_['right']

    #creating my 2 objects/sensors and calculating their membership values and storing them in (rfs/rbs)
    rfs = sensor(fr).fuzzification()
    rbs = sensor(r).fuzzification()
    print("These are the membership values", rfs, rbs)

    #calculating my firing strenght list
    firing = defuzzification(rfs, rbs)
    print("The firing strength", defuzzification(rfs, rbs))

    #Final step is defuzzifcation and getting the speed and direction
    s, d = Defuzz(firing)
    print(f"speed:{s},direction:{d}")
    msg.linear.x = s
    msg.angular.z = d*-1
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
