'''
macad_agent.py: MacadAgent inherit from AutonomousAgent.py. The purpose is to make macad-gym current config works.
__author__: Morphlng
'''

import carla
import weakref
from macad_gym.core.agents.autonomous_agent import AutonomousAgent


def sensor_name_to_bp(camera_type):
    """Convert sensor name to blueprint
    """
    if "rgb" in camera_type:
        return "sensor.camera.rgb"
    elif "depth" in camera_type:
        return "sensor.camera.depth"
    elif "semseg" in camera_type:
        return "sensor.camera.semantic_segmentation"
    elif "lidar" in camera_type:
        return "sensor.lidar.ray_cast"
    else:
        raise ValueError("Unknown sensor name: {}".format(camera_type))


class MacadAgent(AutonomousAgent):
    """
        All agent used in macad-gym should inherit from this class.

        You can override setup(), run_step() and destroy() methods

        Note:
            call super().setup(actor_config) in your setup() method to parse sensors from actor_config
    """

    _camera_transforms = [
        {"x": 1.8, "y": 0.0, "z": 1.7, "pitch": 0.0, "yaw": 0.0, "roll": 0.0},
        {"x": -5.5, "y": 0.0, "z": 2.8, "pitch": -15.0, "yaw": 0.0, "roll": 0.0},
    ]

    def setup(self, config):
        self.simulator = config.pop("simulator")
        self.actor_config = config

        self.obs = None
        self.sensor_list = []

        weak_self = weakref.ref(self)
        self.callbacks = [self.simulator.add_callback(
            lambda snapshot: MacadAgent.on_carla_tick(weak_self))]
        self.parse_sensors()

    def sensors(self):
        return self.sensor_list

    def parse_sensors(self):
        """Parse sensors from actor config to make it compatible for setup_sensors in AgentWrapper
        """
        camera_types = self.actor_config.get("camera_type", [])

        if not isinstance(camera_types, list):
            camera_types = [camera_types]

        for camera_type in camera_types:
            sensor_spec = {
                'id': camera_type,
                'type': sensor_name_to_bp(camera_type),
                'width': self.actor_config["x_res"],
                'height': self.actor_config["y_res"],
                'attachment_type': carla.AttachmentType.Rigid,
            }

            # Use default values to meet AgentWrapper's requirement
            if sensor_spec['type'].startswith('sensor.camera'):
                sensor_spec.update({'fov': 90})
            elif sensor_spec['type'].startswith('sensor.lidar'):
                sensor_spec.update(
                    {
                        'range': 10.0,
                        'rotation_frequency': 10.0,
                        'channels': 32,
                        'upper_fov': 10.0,
                        'lower_fov': -30.0,
                        'points_per_second': 56000,
                    }
                )

            camera_pos = self.actor_config.get("camera_position", 0)
            if isinstance(camera_pos, dict):
                sensor_spec.update(camera_pos)
            else:
                sensor_spec.update(self._camera_transforms[camera_pos])

            self.sensor_list.append(sensor_spec)

    def __call__(self, action=None):
        """
        Execute the agent call, e.g. agent()
        Returns the next vehicle controls
        """
        timestamp = self.simulator._game_time.get_time()
        control = self.run_step(self.obs, timestamp)
        control.manual_gear_shift = False
        return control

    def destroy(self):
        for callback in self.callbacks:
            self.simulator.remove_callback(callback)

        self.simulator = None
        self.obs = None
        self.actor_config = None
        self.sensor_list = []
        self.callbacks = []

    @staticmethod
    def on_carla_tick(weak_self):
        """Update obs on carla tick
        """
        self = weak_self()
        if not self:
            return

        if not self.sensor_interface._new_data_buffers.empty():
            self.obs = self.sensor_interface.get_data()

        actor_id = self.actor_config.get("actor_id", "global")
        self.simulator._sensor_provider.update_camera_data(actor_id, self.obs)

        # TODO: check actor_config["log_images"] to save image
