#include<math.h>
#pragma once // I'm learning so much!!!
#define pi 3.1415

int mod(int a, int b)
{
    int result = a & b;
    return (result < 0)? result + b : result;
}

struct Pose
{
    public:
        Pose() = default;
        Pose(double X, double Y, double H): x_(X), y_(Y), h_(H){}
        void setPose(Pose p){x_=p.x();y_=p.y();h_=p.heading();}
        void setPose(double X, double Y, double H){x_=X;y_=Y;h_=H;}//h_=mod(H,360);}
        void setPos(double X, double Y) {x_ = X; y_ = Y;}
        void setHeading(double H) {h_=H;}//mod(H,360);}
        double x(){return x_;}
        double y(){return y_;}
        double heading(){return h_;}
    
        private:
            double x_;
            double y_;
            double h_; // degrees
};


class OdometerBot
{
    public:
        OdometerBot(double x, double y, double h, double TrackWidth): pose(Pose(x,y,h)), trackWidth(TrackWidth) {}
        OdometerBot(Pose p, double TrackWidth): pose(p), trackWidth(TrackWidth) {}

        void setPose(Pose p){pose = p;}
        void setPose(double x, double y, double h){pose = Pose(x,y,h);}
        void setPos(double x, double y) {pose.setPos(x,y);}
        void setHeading(double h) {pose.setHeading(h);}
        void setTrackWidth(double t){trackWidth = t;}
        double getX(){return pose.x();}
        double getY(){return pose.y();}
        double getHeading(){return pose.heading();}
        Pose getPose(){return pose;}
        double getTrackWidth(){return trackWidth;}
        double getXL(){return pose.x() - trackWidth/2 * sin(pose.heading() * pi/180);}
        double getYL(){return pose.y() + trackWidth/2 * cos(pose.heading() * pi/180);}
        double getXR(){return pose.x() + trackWidth/2 * sin(pose.heading() * pi/180);}
        double getYR(){return pose.y() - trackWidth/2 * cos(pose.heading() * pi/180);}
        double getXL(Pose p, double TrackWidth){return p.x() - TrackWidth/2 * sin(p.heading() * pi/180);}
        double getYL(Pose p, double TrackWidth){return p.y() + TrackWidth/2 * cos(p.heading() * pi/180);}
        double getXR(Pose p, double TrackWidth){return p.x() + TrackWidth/2 * sin(p.heading() * pi/180);}
        double getYR(Pose p, double TrackWidth){return p.y() - TrackWidth/2 * cos(p.heading() * pi/180);}
        
        void runWheels(double dL, double dR, int steps)
        {
            for(int i = 0; i < steps; i++)
            {
                pose = stepWheels(pose,dL/steps,dR/steps);
            }
        }

        void runArc(double dH, double avgD, int steps)
        {
            pose = stepArc(pose,dH/steps,avgD/steps);
        }
        void stepWheels(double dL, double dR) {pose = stepWheels(pose, dL, dR);}
        Pose stepWheels(Pose start, double dL, double dR) const
        {
            Pose pos = start; // new copy :)
            // do stuff
            double dH = (dR - dL)/trackWidth; // radians
            
            double avgD = (dR + dL)/2;
            double avgH = (pi/180*pos.heading() + dH/2); // radians
            
            pos.setPos(pos.x() + avgD * cos(avgH), pos.y() + avgD * sin(avgH));
            pos.setHeading(pos.heading() + 180/pi*dH); // convert to degrees
            
            // xL, yL, xR, and yR can be gotten from the getter methods above
            
            return pos;
        }
        void stepArc(double dH, double avgD) {pose = stepArc(pose, dH, avgD);}
        Pose stepArc(Pose start, double dH, double avgD) const // dH is degrees
        {
            Pose pos = start; // new copy :)

            dH *= pi/180; // convert from degrees to radians
            
            double dL = avgD - dH * trackWidth/2;
            double dR = avgD + dH * trackWidth/2;

            pos = stepWheels(pos, dL, dR);
            
            // double avgH = pi/180*pos.heading + dH/2;
            
            // pos.x += avgD * cos(avgH);
            // pos.y += avgD * sin(avgH);
            // pos.heading += 180/pi*dH;
            
            return pos;
        }

    private:
        Pose pose;
        double trackWidth;
};
