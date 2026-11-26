#include<math.h>
#pragma once // I'm learning so much!!!
#define pi 3.1415

struct Pose
{
    Pose() = default;
    Pose(double X, double Y, double H): x(X), y(Y), heading(H){}
    double x;
    double y;
    double heading; // degrees
};


class OdometerBot
{
    public:
        OdometerBot(double x, double y, double h, double TrackWidth): pose(Pose(x,y,h)), trackWidth(TrackWidth) {}
        OdometerBot(Pose p, double TrackWidth): pose(p), trackWidth(TrackWidth) {}

        void setPose(Pose p){pose = p;}
        void setPose(double x, double y, double h){pose = Pose(x,y,h);}
        void setPos(double x, double y) {pose.x = x; pose.y = y;}
        void setHeading(double h) {pose.heading = h;}
        void setTrackWidth(double t){trackWidth = t;}
        double getX(){return pose.x;}
        double getY(){return pose.y;}
        double getHeading(){return pose.heading;}
        Pose getPose(){return pose;}
        double getTrackWidth(){return trackWidth;}
        double getXL(){return pose.x - trackWidth/2 * sin(pose.heading * pi/180);}
        double getYL(){return pose.y + trackWidth/2 * cos(pose.heading * pi/180);}
        double getXR(){return pose.x + trackWidth/2 * sin(pose.heading * pi/180);}
        double getYR(){return pose.y - trackWidth/2 * cos(pose.heading * pi/180);}
        double getXL(Pose p, double TrackWidth){return p.x - TrackWidth/2 * sin(p.heading * pi/180);}
        double getYL(Pose p, double TrackWidth){return p.y + TrackWidth/2 * cos(p.heading * pi/180);}
        double getXR(Pose p, double TrackWidth){return p.x + TrackWidth/2 * sin(p.heading * pi/180);}
        double getYR(Pose p, double TrackWidth){return p.y - TrackWidth/2 * cos(p.heading * pi/180);}
        
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
            double avgH = (pi/180*pose.heading + dH/2); // radians
            
            pos.x += avgD * cos(avgH);
            pos.y += avgD * sin(avgH);
            pos.heading += 180/pi*dH; // convert to degrees
            
            // xL, yL, xR, and yR can be gotten from the getter methods above
            
            return pos;
        }
        void stepArc(double dH, double avgD) {pose = stepArc(pose, dH, avgD);}
        Pose stepArc(Pose start, double dH, double avgD) const // dH is degrees
        {
            Pose pos = start; // new copy :)

            dH *= pi/180; // convert from degrees to radians
            
            // double dL = avgD - dH * trackWidth/2;
            // double dR = avgD + dH * trackWidth/2;
            
            double avgH = pi/180*pos.heading + dH/2;
            
            pos.x += avgD * cos(avgH);
            pos.y += avgD * sin(avgH);
            pos.heading += 180/pi*dH;
            
            return pos;
        }

    private:
        Pose pose;
        double trackWidth;
};
