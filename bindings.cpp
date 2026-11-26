#include<pybind11/pybind11.h>
#include<pybind11/stl.h>
#include "OdometerBot.h"

PYBIND11_MODULE(backend, m)
{
    pybind11::class_<OdometerBot>(m,"OdometerBot")
        .def(pybind11::init<double, double, double, double>())
        .def(pybind11::init<Pose, double>())
        .def("setPose",pybind11::overload_cast<Pose>(&OdometerBot::setPose))
        .def("setPose",pybind11::overload_cast<double, double, double>(&OdometerBot::setPose))
        .def("setPos",&OdometerBot::setPos)
        .def("setHeading",&OdometerBot::setHeading)
        .def("setTrackWidth",&OdometerBot::setTrackWidth)
        .def("getX",&OdometerBot::getX)
        .def("getY",&OdometerBot::getY)
        .def("getHeading",&OdometerBot::getHeading)
        .def("getPose",&OdometerBot::getPose)
        .def("getTrackWidth",&OdometerBot::getTrackWidth)
        .def("getXL",pybind11::overload_cast<>(&OdometerBot::getXL))
        .def("getXL",pybind11::overload_cast<Pose, double>(&OdometerBot::getXL))
        .def("getYL",pybind11::overload_cast<>(&OdometerBot::getYL))
        .def("getYL",pybind11::overload_cast<Pose, double>(&OdometerBot::getYL))
        .def("getXR",pybind11::overload_cast<>(&OdometerBot::getXR))
        .def("getXR",pybind11::overload_cast<Pose, double>(&OdometerBot::getXR))
        .def("getYR",pybind11::overload_cast<>(&OdometerBot::getYR))
        .def("getYR",pybind11::overload_cast<Pose, double>(&OdometerBot::getYR))
        .def("runWheels",&OdometerBot::runWheels)
        .def("runArc",&OdometerBot::runArc)
        .def("stepWheels",pybind11::overload_cast<Pose, double, double>(&OdometerBot::stepWheels, pybind11::const_))
        .def("stepWheels",pybind11::overload_cast<double, double>(&OdometerBot::stepWheels))
        .def("stepArc",pybind11::overload_cast<Pose, double, double>(&OdometerBot::stepArc, pybind11::const_))
        .def("stepArc",pybind11::overload_cast<double, double>(&OdometerBot::stepArc));

    pybind11::class_<Pose>(m,"Pose")
        .def(pybind11::init<>())
        .def(pybind11::init<double, double, double>());

}