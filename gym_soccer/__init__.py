import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)

register(
    id='Soccer-v0',
    entry_point='gym_soccer.envs:SoccerEnv',
    # Previously timestep_limit, changed due to upgrade of gym
    max_episode_steps=1000, 
    # timestep_limit=1000,
    reward_threshold=1.0,
    nondeterministic = True,
)

register(
    id='SoccerEmptyGoal-v0',
    entry_point='gym_soccer.envs:SoccerEmptyGoalEnv',
    # Previously timestep_limit, changed due to upgrade of gym
    max_episode_steps=1000, 
    # timestep_limit=1000,
    reward_threshold=10.0,
    nondeterministic = True,
)

register(
    id='SoccerAgainstKeeper-v0',
    entry_point='gym_soccer.envs:SoccerAgainstKeeperEnv',
    # Previously timestep_limit, changed due to upgrade of gym
    max_episode_steps=1000, 
    # timestep_limit=1000,
    reward_threshold=8.0,
    nondeterministic = True,
)
