#include "ros/callback_queue.h"
#include "ros/ros.h"
#include "ros/subscribe_options.h"
#include "std_msgs/Float32.h"
#include <functional>
#include <gazebo/common/common.hh>
#include <gazebo/gazebo.hh>
#include <gazebo/msgs/msgs.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo/transport/transport.hh>
#include <ignition/math/Vector3.hh>
#include <thread>

namespace gazebo {
class FluidResistance : public ModelPlugin {
public:
  void Load(physics::ModelPtr _parent, sdf::ElementPtr _sdf) {

    if (_sdf->HasElement("fluid_resistanceTopicName")) {
      this->fluid_resistanceTopicName =
          _sdf->Get<std::string>("fluid_resistanceTopicName");
      ROS_WARN("This plugin is running successfully");
    } else {
      ROS_WARN("No Topic Given name given, setting default name %s",
               this->fluid_resistanceTopicName.c_str());
    }

    if (_sdf->HasElement("NameLinkToApplyResistance")) {
      this->NameLinkToApplyResistance =
          _sdf->Get<std::string>("NameLinkToApplyResistance");
    } else {
      ROS_WARN("No NameLinkToApplyResistance Given name given, setting default "
               "name %s",
               this->NameLinkToApplyResistance.c_str());
    }

    if (_sdf->HasElement("rate")) {
      this->rate = _sdf->Get<double>("rate");
    } else {
      ROS_WARN("No rate Given name given, setting default "
               "name %f",
               this->rate);
    }

    // Store the pointer to the model
    this->model = _parent;
    this->world = this->model->GetWorld();
    this->link_to_apply_resistance =
        this->model->GetLink(this->NameLinkToApplyResistance);

    // Listen to the update event. This event is broadcast every
    // simulation iteration.
    this->updateConnection = event::Events::ConnectWorldUpdateBegin(
        std::bind(&FluidResistance::OnUpdate, this));

    // Create a topic name
    // std::string fluid_resistance_index_topicName = "/fluid_resistance_index";

    // Initialize ros, if it has not already bee initialized.
    if (!ros::isInitialized()) {
      int argc = 0;
      char **argv = NULL;
      ros::init(argc, argv, "model_mas_controler_rosnode",
                ros::init_options::NoSigintHandler);
    }

    // Create our ROS node. This acts in a similar manner to
    // the Gazebo node
    this->rosNode.reset(new ros::NodeHandle("model_mas_controler_rosnode"));

#if (GAZEBO_MAJOR_VERSION >= 8)
    this->last_time = this->world->SimTime().Float();
#else
    this->last_time = this->world->GetSimTime().Float();
#endif

    // Freq
    ros::SubscribeOptions so = ros::SubscribeOptions::create<std_msgs::Float32>(
        this->fluid_resistanceTopicName, 1,
        boost::bind(&FluidResistance::OnRosMsg, this, _1), ros::VoidPtr(),
        &this->rosQueue);
    this->rosSub = this->rosNode->subscribe(so);

    // Spin up the queue helper thread.
    this->rosQueueThread =
        std::thread(std::bind(&FluidResistance::QueueThread, this));

    ROS_WARN("Loaded FluidResistance Plugin with parent...%s, With Fluid "
             "Resistance = %f "
             "Started ",
             this->model->GetName().c_str(), this->fluid_resistance_index);
  }

  // Called by the world update start event
public:
  void OnUpdate() {
    float period = 1.0 / this->rate;

    // Get simulator time
#if (GAZEBO_MAJOR_VERSION >= 8)
    float current_time = this->world->SimTime().Float();
#else
    float current_time = this->world->GetSimTime().Float();
#endif
    float dt = current_time - this->last_time;

    if (dt <= period){
        ROS_DEBUG(">>>>>>>>>>TimePassed = %f, TimePeriod =%f ",dt, period);
        return;
    }else{
        this->last_time = current_time;
        this->ApplyResistance();
    }


  }

public:
  void SetResistance(const double &_force) {
    this->fluid_resistance_index = _force;
    ROS_WARN("model_fluid_resistance_index changed >> %f",
             this->fluid_resistance_index);
  }

  void UpdateLinearVel() {
#if (GAZEBO_MAJOR_VERSION >= 8)
    this->now_lin_vel = this->model->RelativeLinearVel();
#else
    this->now_lin_vel = this->model->GetRelativeLinearVel();
#endif
  }

  void ApplyResistance() {

    this->UpdateLinearVel();

#if (GAZEBO_MAJOR_VERSION >= 8)
    ignition::math::Vector3d force, torque;
#else
    math::Vector3 force, torque;
#endif

    //ROS_WARN("LinearSpeed = [%f,%f,%f] ",this->now_lin_vel.x, this->now_lin_vel.y, this->now_lin_vel.z);

    //Uncomment next three lines in future if necessary
    //force.x = -1.0 * this->fluid_resistance_index * this->now_lin_vel.x;
    //force.y = -1.0 * this->fluid_resistance_index * this->now_lin_vel.y;
    //force.z = -1.0 * this->fluid_resistance_index * this->now_lin_vel.z;

    double x = -1.0 * this->fluid_resistance_index * 10;
    double y = -1.0 * this->fluid_resistance_index * 0;
    double z = -1.0 * this->fluid_resistance_index * 0;

    // Changing the mass
    this->link_to_apply_resistance->AddRelativeForce(ignition::math::Vector3d(x, y, z));
#if (GAZEBO_MAJOR_VERSION >= 8)
    this->link_to_apply_resistance->AddRelativeTorque(
        torque -
        this->link_to_apply_resistance->GetInertial()->CoG().Cross(force));
#else
    this->link_to_apply_resistance->AddRelativeTorque(
        torque -
        this->link_to_apply_resistance->GetInertial()->GetCoG().Cross(force));
#endif

    //ROS_WARN("FluidResistanceApplying = [%f,%f,%f] ",force.x, force.y, force.z);
  }

public:
  void OnRosMsg(const std_msgs::Float32ConstPtr &_msg) {
    this->SetResistance(_msg->data);
  }

  /// \brief ROS helper function that processes messages
private:
  void QueueThread() {
    static const double timeout = 0.01;
    while (this->rosNode->ok()) {
      this->rosQueue.callAvailable(ros::WallDuration(timeout));
    }
  }

  // Pointer to the model
private:
  physics::ModelPtr model;

  // Pointer to the update event connection
private:
  event::ConnectionPtr updateConnection;

  // Mas of model
  double fluid_resistance_index = 1000.0;

  /// \brief A node use for ROS transport
private:
  std::unique_ptr<ros::NodeHandle> rosNode;

  /// \brief A ROS subscriber
private:
  ros::Subscriber rosSub;
  /// \brief A ROS callbackqueue that helps process messages
private:
  ros::CallbackQueue rosQueue;
  /// \brief A thread the keeps running the rosQueue
private:
  std::thread rosQueueThread;

  /// \brief A ROS subscriber
private:
  physics::LinkPtr link_to_apply_resistance;

private:
  std::string fluid_resistanceTopicName = "fluid_resistance";

private:
  std::string NameLinkToApplyResistance = "base_link";

private:
#if (GAZEBO_MAJOR_VERSION >= 8)
  ignition::math::Vector3d now_lin_vel;
#else
  math::Vector3 now_lin_vel;
#endif

private:
  double rate = 1.0;

private:
  float last_time = 0.0;

private:
  /// \brief The parent World
  physics::WorldPtr world;
};

// Register this plugin with the simulator
GZ_REGISTER_MODEL_PLUGIN(FluidResistance)
} // namespace gazebo
