
class Hopper(object):

    @staticmethod
    def side_to_face(side):
        """
        将方块的侧面转换为朝向。
        例如B在A的西方，则B需要朝向东面才能对准A。
        :param int side: 面向
        :rtype: int
        """
        return side + (1 if side & 1 == 0 else -1)

    @staticmethod
    def is_active(states):
        """
        判断漏斗是否可活动，即是否没有被红石锁定。
        :param dict states: 漏斗的方块状态
        :rtype: bool
        """
        return not states['toggle_bit']

    @staticmethod
    def is_target_face(states, facing):
        """
        判断漏斗是否为指定朝向。
        :param dict states: 漏斗的方块状态
        :param int facing: 朝向
        :rtype: bool
        """
        return states['facing_direction'] == facing

    @staticmethod
    def can_take_out(states, facing):
        """
        判断漏斗是否可以将物品输出到对应朝向的对象中。
        :param dict states: 漏斗的方块状态
        :param int facing: 输出的朝向
        :rtype: bool
        """
        return Hopper.is_active(states) and Hopper.is_target_face(states, facing)

    @staticmethod
    def can_take_in(states):
        """
        判断漏斗是否可以从上方对象输入物品。
        :param dict states: 漏斗的方块状态
        :rtype: bool
        """
        return Hopper.is_active(states)