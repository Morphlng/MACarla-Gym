from macad_gym.envs import MultiCarlaEnv

configs = {
    "scenarios": {
        "map": "Town03",
        "actors": {
            "car1": {
                "start": [170.5, 80, 0.4],
                "end": [144, 59, 0]
            },
            "car2": {
                "start": [188, 59, 0.4],
                "end": [167, 75.7, 0.13],
            },
            "car3": {
                "start": [147.6, 62.6, 0.4],
                "end": [191.2, 62.7, 0],
            }
        },
        "weather_distribution": [0],
        # "max_steps": 500,
        "max_time": 60,         # seconds
        "num_vehicles": 0,     # The number of npc vehicles
        "num_pedestrians": 0,
    },
    "env": {
        "server_map": "/Game/Carla/Maps/Town03",
        "render": True,
        "render_x_res": 800,
        "render_y_res": 600,
        "obs_x_res": 168,
        "obs_y_res": 168,
        "framestack": 1,
        "discrete_actions": True,
        "squash_action_logits": False,
        "verbose": False,
        "use_depth_camera": False,
        "send_measurements": False,
        "enable_planner": True,
        "spectator_loc": [140, 68, 9],
        "sync_server": True,
        "fixed_delta_seconds": 0.05,
        "global_observation": {
            "camera_type": "semseg",
            "x_res": 512,
            "y_res": 512,
            "camera_position": {"x": 171, "y": 70, "z": 32, "pitch": -90, "yaw": -90, "roll": 0},
            "render": True
        }
    },
    "actors": {
        "car1": {
            "type": "vehicle_4W",
            "enable_planner": True,
            "convert_images_to_video": False,
            "early_terminate_on_collision": True,
            "reward_function": "corl2017",
            "scenarios": "SSUI3C_TOWN3_CAR1",
            "manual_control": False,
            "auto_control": True,
            "camera_type": "semseg",
            "collision_sensor": "on",
            "lane_sensor": "on",
            "log_images": False,
            "log_measurements": False,
            "render": True,
            "use_depth_camera": False,
            "send_measurements": False,
        },
        "car2": {
            "type": "vehicle_4W",
            "enable_planner": True,
            "convert_images_to_video": False,
            "early_terminate_on_collision": True,
            "reward_function": "corl2017",
            "scenarios": "SSUI3C_TOWN3_CAR2",
            "manual_control": False,
            "auto_control": True,
            "camera_type": "rgb",
            "collision_sensor": "on",
            "lane_sensor": "on",
            "log_images": False,
            "log_measurements": False,
            "render": True,
            "use_depth_camera": False,
            "send_measurements": False,
        },
        "car3": {
            "type": "vehicle_4W",
            "enable_planner": True,
            "convert_images_to_video": False,
            "early_terminate_on_collision": True,
            "reward_function": "corl2017",
            "scenarios": "SSUI3C_TOWN3_CAR3",
            "manual_control": False,
            "auto_control": True,
            "camera_type": "depth",
            "collision_sensor": "on",
            "lane_sensor": "on",
            "log_images": False,
            "log_measurements": False,
            "render": True,
            "use_depth_camera": False,
            "send_measurements": False,
        },
    },
}

if __name__ == "__main__":
    env = MultiCarlaEnv(configs)

    for ep in range(1):
        obs = env.reset()

        total_reward_dict = {}
        action_dict = {}

        env_config = configs["env"]
        actor_configs = configs["actors"]
        for actor_id in actor_configs.keys():
            total_reward_dict[actor_id] = 0
            if env._discrete_actions:
                action_dict[actor_id] = 4  # Brake
            else:
                action_dict[actor_id] = [0, 0]  # test values

        i = 0
        done = {"__all__": False}
        while not done["__all__"]:
            i += 1
            obs, reward, done, info = env.step(action_dict)

            for actor_id in total_reward_dict.keys():
                total_reward_dict[actor_id] += reward[actor_id]
            print(":{}\n\t".join(["Step#", "rew", "ep_rew",
                                  "done{}"]).format(i, reward,
                                                    total_reward_dict, done))
