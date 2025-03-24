# Configure image
ARG PYTHON_VERSION=3.10

FROM python:${PYTHON_VERSION}-slim


# Install apt dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake \
    libglib2.0-0 libgl1-mesa-glx libegl1-mesa ffmpeg \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN ln -s /usr/bin/python${PYTHON_VERSION} /usr/bin/python
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN echo "source /opt/venv/bin/activate" >> /root/.bashrc

# Install LeRobot
COPY . /lerobot-gen72
WORKDIR /lerobot-gen72


RUN pip install --upgrade --no-cache-dir pip
RUN pip install --no-cache-dir ".[aloha, koch]"
RUN pip install mujoco opencv-python dynamixel_sdk ffmpeg

# Set EGL as the rendering backend for MuJoCo
ENV MUJOCO_GL="egl"

# Execute in bash shell rather than python
CMD ["bash"]
