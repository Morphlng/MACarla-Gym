# MACarla-Gym

This repo is a fork from [praveen-palanisamy/macad-gym](https://github.com/praveen-palanisamy/macad-gym). We've done some modification to the data layer and some improvement over performance. Due to the inconsistency of some behavior, this repo **will not** merge to macad-gym's master branch. 

# Integration with MARLlib

Multi-Agent RLlib (MARLlib) is a comprehensive Multi-Agent Reinforcement Learning algorithm library based on Ray and one of its toolkits RLlib. It provides MARL research community with a unified platform for building, training, and evaluating MARL algorithms.

Our [fork of MARLlib](https://github.com/Morphlng/MARLlib) provide the integration of Macad-Gym, so you can train your RL Agent in one line. Below will show you the setup steps:

1. Create a new conda environment.

    ```bash
    conda create -n marllib python=3.8

    conda activate marllib
    ```

2. Install Macad-Gym.

    ```bash
    pip install carla==0.9.13
    pip install git+https://github.com/Morphlng/MACarla-Gym.git
    ```

    The above lines will install this repo as your Macad-Gym, instead of the Pypi version.

3. Install MARLlib

    First you'll need to install Pytorch<=1.9.1, see [official tutorial](https://pytorch.org/get-started/previous-versions/#linux-and-windows-11) for more platform support. Then, install ray==1.8.0 with tune and rllib.

    ```bash
    pip install torch==1.9.1+cu111 torchvision==0.10.1+cu111 torchaudio==0.9.1 -f https://download.pytorch.org/whl/torch_stable.html
    
    pip install ray==1.8.0
    pip install ray[tune]
    pip install ray[rllib]
    ```

    Second, clone MARLlib to a local directory. Install this local repo using pip and do the patch.

    ```bash
    git clone https://github.com/Morphlng/MARLlib.git

    cd MARLlib

    pip install -e .

    python ./patch/add_patch.py -y
    ```

    Finally, you should check the version of these libraries:

    ```bash
    pip install icecream && pip install supersuit && pip install gym==0.21.0 && pip install importlib-metadata==4.13.0
    ```

    For the combination of Macad-Gym and MARLlib, these steps above should prepare you well. However, if you want to use other environment integrated in MARLlib, you may have to look into the official [document of MARLlib](https://marllib.readthedocs.io/en/latest/handbook/env.html)

4. Start training

    You can use this single line to start training. Currently only mappo has been tested.

    ```bash
    cd MARLlib

    python marl/main.py --env_config=macad --algo_config=mappo --finetuned
    ```

    If you want to change the scenario of Macad or do some other finetuning, the following two files are the one you'll have to change:
    - MARLlib/envs/base_envs/config/macad.yaml
    - MARLlib/marl/algos/hyperparams/finetuned/macad/mappo.yaml