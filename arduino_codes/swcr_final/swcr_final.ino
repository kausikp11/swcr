
#include <ArduinoHardware.h>
#include <ros.h>
#include <geometry_msgs/Twist.h>
#include <Motor.h>
#include <HcSR04.h>
#include <Servo.h>
#include <sensor_msgs/Range.h>
#include <std_msgs/Float64.h>


ros::NodeHandle nh;
std_msgs::Float64 str_msg;


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


void msg_init(sensor_msgs::Range &range_name, char *frame_id_name)
{
  range_name.radiation_type = sensor_msgs::Range::ULTRASOUND;
  range_name.header.frame_id = frame_id_name;
  range_name.field_of_view = 0.5;
  range_name.min_range = 0.02;
  range_name.max_range = 3.2;
}


void messageCb( const geometry_msgs::Twist& msg) {
  speed_ang = msg.angular.z;
  speed_lin = msg.linear.x;
  w_r = (speed_lin / wheel_rad) + ((speed_ang * wheel_sep) / (2.0 * wheel_rad));
  w_l = (speed_lin / wheel_rad) - ((speed_ang * wheel_sep) / (2.0 * wheel_rad));
}


sensor_msgs::Range sonar1;
sensor_msgs::Range sonar2;
sensor_msgs::Range sonar3;
sensor_msgs::Range sonar4;
sensor_msgs::Range sonar5;


ros::Subscriber<geometry_msgs::Twist> sub("cmd_vel", &messageCb );
ros::Publisher pub_sonar1("sonar1", &sonar1);
ros::Publisher pub_sonar2("sonar2", &sonar2);
ros::Publisher pub_sonar3("sonar3", &sonar3);
ros::Publisher pub_sonar4("sonar4", &sonar4);
ros::Publisher pub_sonar5("sonar5", &sonar5);


void setup() {


  nh.initNode();


  nh.advertise(pub_sonar1);
  nh.advertise(pub_sonar2);
  nh.advertise(pub_sonar3);
  nh.advertise(pub_sonar4);
  nh.advertise(pub_sonar5);


  nh.subscribe(sub);


  motor_left.attach(22);
  motor_right.attach(23);

  //  Serial.begin(9600);

}


void loop() {


  msg_init(sonar1, "sonar1");
  msg_init(sonar2, "sonar2");
  msg_init(sonar3, "sonar3");
  msg_init(sonar4, "sonar4");
  msg_init(sonar5, "sonar5");


  l = sonar1.range = Left.sense() / 100;
  fl = sonar2.range = FrontLeft.sense() / 100;
  m = sonar3.range = FrontMiddle.sense() / 100;
  fr = sonar4.range = FrontRight.sense() / 100;
  r = sonar5.range = Right.sense() / 100;


  pub_sonar1.publish(&sonar1);
  pub_sonar2.publish(&sonar2);
  pub_sonar3.publish(&sonar3);
  pub_sonar4.publish(&sonar4);
  pub_sonar5.publish(&sonar5);


  //  Serial.print("\tLeft:"); Serial.print(sonar1.range);
  //  Serial.print("\tFront Left:"); Serial.print(sonar2.range);
  //  Serial.print("\tMiddle:"); Serial.print(sonar3.range);
  //  Serial.print("\tfront Right:"); Serial.print(sonar4.range); \
  //  Serial.print("\tRight:"); Serial.print(sonar5.range); Serial.print("\n");

  front.Motor_move((w_l * 10), (w_r * 10));
  rear.Motor_move((w_l * 10), (w_r * 10));


  nh.spinOnce();
  //  delay(1);
}
