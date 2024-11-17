#include <functional>
#include <gazebo/gazebo.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo/common/common.hh>
#include <ignition/math/Vector3.hh>
#include <random>
#include <iostream>
#include <string>
#include <thread>
#include <chrono>
#include <time.h>

namespace gazebo
{
    class ModelPush : public ModelPlugin
    {
        public: void Load(physics::ModelPtr _parent, sdf::ElementPtr /*_sdf*/)
                {
                    this->model = _parent;
                    this->updateConnection = event::Events::ConnectWorldUpdateBegin(std::bind(&ModelPush::OnUpdate, this));
                }
        public: void OnUpdate()
                {
                    srand( (signed)time( NULL ) );
                    double x =  ( ((((float) rand()/RAND_MAX)*2) - 1))/16;
                    double y =  ( ((((float) rand()/RAND_MAX)*2) - 1))/16;

                    //double x_dist = ( ((((float) rand()/RAND_MAX)*2) - 1)) / 4;
                    //double y_dist = ( ((((float) rand()/RAND_MAX)*2) - 1)) / 4;

                    //std::mt19937 gen (123);
                    //std::uniform_real_distribution<double> dis(0.0, 1.0);
                    //double x = dis(gen);
                    //double y = dis(gen);
                    //int z = dis(gen);
                    //std::cout << "Z: " << z << std::endl;
                    this->model->SetLinearVel(ignition::math::Vector3d(0.08, 0, 0));
                    this->model->SetAngularVel(ignition::math::Vector3d(x, y, 0));
                    //std::this_thread::sleep_for(std::chrono::milliseconds(100));
                    }
                
        private: physics::ModelPtr model;
        private: event::ConnectionPtr updateConnection;
    };
    GZ_REGISTER_MODEL_PLUGIN(ModelPush)
}
