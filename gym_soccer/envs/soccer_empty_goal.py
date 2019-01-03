import logging
import math
from gym_soccer.envs.soccer_env import SoccerEnv

try:
    import hfo_py
except ImportError as e:
    raise error.DependencyNotInstalled("{}. (HINT: you can install HFO dependencies with 'pip install gym[soccer].)'".format(e))

logger = logging.getLogger(__name__)

class SoccerEmptyGoalEnv(SoccerEnv):
    """
    SoccerEmptyGoal tasks the agent with approaching the ball,
    dribbling, and scoring a goal. Rewards are given as the agent nears
    the ball, kicks the ball towards the goal, and scores a goal.

    """
    def __init__(self):
        super(SoccerEmptyGoalEnv, self).__init__()
        self.old_ball_prox = 0
        self.old_kickable = 0
        self.old_ball_dist_goal = 0
        self.got_kickable_reward = False
        self.first_step = True

    def _configure_environment(self):
        """
        Provides a chance for subclasses to override this method and supply
        a different server configuration. 
        """
        # Set the random seed, need to divide to make the number
        # smaller, otherwise, the server will raise error
        seed = self.seed()[0] / 1e13
        kwargs = dict(
            # This should be the same length in the __init__.py
            frames_per_trial=1000,
            # To make the problem simpler, we do not use this
            # value. Thus, set to a value is greater than 
            # frames_per_trial
            untouched_time=1200,
            offense_agents=1,
            defense_agents=0,
            offense_npcs=0,
            defense_npcs=0,
            sync_mode=True,
            port=6000,
            offense_on_ball=0,
            fullstate=True,
            seed=seed,
            ball_x_min=0.0,
            ball_x_max=0.2,
            verbose=False,
            log_game=False,
            log_dir="log"
        )
        self._start_hfo_server(**kwargs)

    def _get_reward(self):
        """
        Agent is rewarded for minimizing the distance between itself and
        the ball, minimizing the distance between the ball and the goal,
        and scoring a goal.
        """
        current_state = self.env.getState()
        ball_proximity = current_state[53]
        goal_proximity = current_state[15]
        ball_dist = 1.0 - ball_proximity
        goal_dist = 1.0 - goal_proximity
        kickable = current_state[12]
        ball_ang_sin_rad = current_state[51]
        ball_ang_cos_rad = current_state[52]
        ball_ang_rad = math.acos(ball_ang_cos_rad)
        if ball_ang_sin_rad < 0:
            ball_ang_rad *= -1.
        goal_ang_sin_rad = current_state[13]
        goal_ang_cos_rad = current_state[14]
        goal_ang_rad = math.acos(goal_ang_cos_rad)
        if goal_ang_sin_rad < 0:
            goal_ang_rad *= -1.
        alpha = max(ball_ang_rad, goal_ang_rad) - min(ball_ang_rad, goal_ang_rad)
        ball_dist_goal = math.sqrt(ball_dist*ball_dist + goal_dist*goal_dist -
                                   2.*ball_dist*goal_dist*math.cos(alpha))
        # Compute the difference in ball proximity from the last step
        if not self.first_step:
            ball_prox_delta = ball_proximity - self.old_ball_prox
            kickable_delta = kickable - self.old_kickable
            ball_dist_goal_delta = ball_dist_goal - self.old_ball_dist_goal
        self.old_ball_prox = ball_proximity
        self.old_kickable = kickable
        self.old_ball_dist_goal = ball_dist_goal

        reward = 0
        if not self.first_step:
            # Reward the agent for moving towards the ball
            reward += ball_prox_delta
            if kickable_delta > 0 and not self.got_kickable_reward:
                reward += 1.
                self.got_kickable_reward = True
            # Reward the agent for kicking towards the goal
            reward += 3.0 * -ball_dist_goal_delta
            # Reward the agent for scoring
            if self.status == hfo_py.GOAL:
                reward += 5.0
        self.first_step = False
        return reward

    def _reset(self):
        self.old_ball_prox = 0
        self.old_kickable = 0
        self.old_ball_dist_goal = 0
        self.got_kickable_reward = False
        self.first_step = True
        return super(SoccerEmptyGoalEnv, self)._reset()
