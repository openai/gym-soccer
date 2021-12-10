import logging
from gym_soccer.envs.soccer_empty_goal import SoccerEmptyGoalEnv

logger = logging.getLogger(__name__)

class SoccerAgainstKeeperEnv(SoccerEmptyGoalEnv):
    """
    SoccerAgainstKeeper initializes the agent most of the way down the
    field with the ball and tasks it with scoring on a keeper.

    Rewards in this task are the same as SoccerEmptyGoal: reward
    is given for kicking the ball close to the goal and extra reward is
    given for scoring a goal.

    """
    def __init__(self, replay_path='./game_log', port=6000):
        super(SoccerAgainstKeeperEnv, self).__init__(replay_path, port)

    def configure_environment(self, replay_path='./game_log', port=6000):
        super(SoccerAgainstKeeperEnv, self)._start_hfo_server(defense_npcs=1,
                                                              offense_on_ball=1,
                                                              ball_x_min=0.6,
                                                              log_dir=replay_path,
                                                              port=port)
