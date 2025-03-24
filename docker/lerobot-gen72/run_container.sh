docker rm -f lerobot-gen72

xhost +

docker run \
  -it \
  -e RIGHT_ARM_IP="192.168.1.19" \
  -e LEFT_ARM_IP="192.168.1.20" \
  -e RIGHT_ARM_PORT="/dev/ttyUSB0" \
  -e LEFT_ARM_PORT="/dev/ttyUSB1" \
  -e DLL_PATH="lerobot/common/robot_devices/robots/libs"\
  --privileged \
  --network=host \
  --name lerobot-gen72 \
  --cap-add=SYS_PTRACE \
  --security-opt seccomp=unconfined \
  --device=/dev/bus/usb:/dev/bus/usb \
  lerobot-gen72:latest 

