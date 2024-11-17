#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/monojit/simulation_ws/src/spawn_robot_tools_pkg"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/monojit/simulation_ws/install/lib/python3/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/monojit/simulation_ws/install/lib/python3/dist-packages:/home/monojit/simulation_ws/build/lib/python3/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/monojit/simulation_ws/build" \
    "/usr/bin/python3" \
    "/home/monojit/simulation_ws/src/spawn_robot_tools_pkg/setup.py" \
     \
    build --build-base "/home/monojit/simulation_ws/build/spawn_robot_tools_pkg" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/monojit/simulation_ws/install" --install-scripts="/home/monojit/simulation_ws/install/bin"