#include <ros.h>
#include <geometry_msgs/Twist.h>
#include <Motor.h>
#include <HcSR04.h>
#include <Servo.h>
#include <swcr/sensor.h>


ros::NodeHandle nh;
swcr::sensor sensor_msg;


Motor front (2, 4, 8, 7, 3, 5);
Motor rear  (9, 10, 12, 11, 13, 6);


HcSR04 Left (44, 45);
HcSR04 FrontLeft (48, 49);
HcSR04 FrontMiddle (52, 53);
HcSR04 FrontRight (50, 51);
HcSR04 Right (46, 47);


Servo motor_left;
Servo motor_right;


int pos = 180;

double w_r = 0, w_l = 0;
//wheel_rad is the wheel radius ,wheel_sep is
double wheel_rad = 0.05, wheel_sep = 0.31;

int lowSpeed = 200;
int highSpeed = 50;

double speed_ang = 0, speed_lin = 0;

double l, fl, m, fr, r;


void messageCb( const geometry_msgs::Twist& msg) {
  speed_ang = msg.angular.z;
  speed_lin = msg.linear.x;
}


ros::Subscriber<geometry_msgs::Twist> sub("cmd_vel", messageCb );
ros::Publisher pub_sonar("sonar", &sensor_msg);


void setup() {


  nh.initNode();


  nh.advertise(pub_sonar);


  nh.subscribe(sub);


  motor_left.attach(22);
  motor_right.attach(23);

  //  Serial.begin(9600);

}


void loop() {

  sensor_msg.l =Left.sense() / 100;
  sensor_msg.fl = FrontLeft.sense() / 100;
  sensor_msg.fm = FrontMiddle.sense() / 100;
  sensor_msg.fr = FrontRight.sense() / 100;
  sensor_msg.r = Right.sense() / 100;


  pub_sonar.publish(&sensor_msg);


  //  Serial.print("\tLeft:"); Serial.print(sonar1.range);
  //  Serial.print("\tFront Left:"); Serial.print(sonar2.range);
  //  Serial.print("\tMiddle:"); Serial.print(sonar3.range);
  //  Serial.print("\tfront Right:"); Serial.print(sonar4.range); \
  //  Serial.print("\tRight:"); Serial.print(sonar5.range); Serial.print("\n");

  w_r = (speed_lin / wheel_rad) + ((speed_ang * wheel_sep) / (2.0 * wheel_rad));
  w_l = (speed_lin / wheel_rad) - ((speed_ang * wheel_sep) / (2.0 * wheel_rad));
  front.Motor_move((w_l * 10), (w_r * 10));
  rear.Motor_move((w_l * 10), (w_r * 10));


  nh.spinOnce();
  delay(500);
}
