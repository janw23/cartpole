import control
import numpy as np


# This is a stub of your solution
# Add your code in any organized way, but please keep the following signatures unchanged
# Solution1 should optimize for speed, Solution2 for effort. Refer to the assignement specification.

GRAVITY = 9.81
MASS_CART = 1.0
MASS_POLE = 0.1
LENGTH_POLE = 0.5
MU_POLE = 0.0

# Keep this signature unchanged for automated testing!
# Returns 2 numpy arrays - matrices A and B
def linearize(
    gravity: float,
    mass_cart: float,
    mass_pole: float,
    length_pole: float,
    mu_pole: float,
):

    # All derivatives are computed at point (0, 0, 0, 0).

    mass_total = mass_cart + mass_pole
    denominator = length_pole * (4 / 3 - mass_pole / mass_total)

    dthetaacc_dtheta = gravity / denominator
    print('dthetaacc_dtheta:', dthetaacc_dtheta)

    dthetaacc_dthetadot = -mu_pole / (mass_pole * length_pole * denominator)
    print('dthetaacc_dthetadot:', dthetaacc_dthetadot)

    dxacc_dtheta = -dthetaacc_dtheta * mass_pole * length_pole / mass_total
    print('dxacc_dtheta:', dxacc_dtheta)

    dxacc_dthetadot = -dthetaacc_dthetadot * mass_pole * length_pole / mass_total
    print('dxacc_dthetadot:', dxacc_dthetadot)

    dthetaacc_df = -1 / (mass_total * denominator)
    print('dthetaacc_df:', dthetaacc_df)

    dxacc_df = (1 - mass_pole * length_pole * dthetaacc_df) / mass_total
    print('dxacc_df:', dxacc_df)

    A = np.zeros((4, 4))
    B = np.zeros((4, 1))

    A[0, 1] = 1
    A[1, 2] = dxacc_dtheta
    A[1, 3] = dxacc_dthetadot
    A[2, 3] = 1
    A[3, 2] = dthetaacc_dtheta
    A[3, 3] = dthetaacc_dthetadot

    B[1, 0] = dxacc_df
    B[3, 0] = dthetaacc_df

    return A, B


class Solution1:
    # Keep this signature unchanged for automated testing!
    # Reminder: implementing arbitrary target_pos is not required, but please try!
    def __init__(self, init_state, target_pos):
        self.target_pos = target_pos
        # minimum time to stability is our goal
        # so we dont care about the energy
        pos = 10
        vel = 1
        ang = 1
        ang_vel = 1
        energy = 0.001
        A, B = linearize(GRAVITY, MASS_CART, MASS_POLE, LENGTH_POLE, MU_POLE)
        self.K, _, _ = control.lqr(A, B, np.eye(4) * np.array([pos, vel, ang, ang_vel]), np.eye(1) * energy)
        

    # Keep this signature unchanged for automated testing!
    # Returns one float - a desired force (u)
    def update(self, state):
        state = state.copy()
        state[0] -= self.target_pos
        return float(-self.K @ state)


class Solution2:
    # Keep this signature unchanged for automated testing!
    # Reminder: implementing arbitrary target_pos is not required, but please try!
    def __init__(self, init_state, target_pos):
        self.target_pos = target_pos
        A, B = linearize(GRAVITY, MASS_CART, MASS_POLE, LENGTH_POLE, MU_POLE)
        self.K, _, _ = control.lqr(A, B, np.eye(4) * np.array([50, 1, 1, 1]), np.eye(1) * 0.1)

    # Keep this signature unchanged for automated testing!
    # Returns one float - a desired force (u)
    def update(self, state):
        state = state.copy()
        state[0] -= self.target_pos
        return float(-self.K @ state)
