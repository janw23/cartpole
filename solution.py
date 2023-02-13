import control
import numpy as np


# This is a stub of your solution
# Add your code in any organized way, but please keep the following signatures unchanged
# Solution1 should optimize for speed, Solution2 for effort. Refer to the assignement specification.

GRAVITY = 9.81
MASS_CART = 1.0
MASS_POLE = 0.1
LENGTH_POLE = 0.5
MU_POLE = 0.001

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
    dthetaacc_dthetadot = -mu_pole / (mass_pole * length_pole * denominator)
    dxacc_dtheta = -dthetaacc_dtheta * mass_pole * length_pole / mass_total
    dxacc_dthetadot = -dthetaacc_dthetadot * mass_pole * length_pole / mass_total
    dthetaacc_df = -1 / (mass_total * denominator)
    dxacc_df = (1 - mass_pole * length_pole * dthetaacc_df) / mass_total

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

        # I have found these parameters by starting with an educated guess and
        # then optimizing them via genetic algorithm.
        # To optimize the time to stability it makes sense to penalize position much more
        # than anything else (energy in particular). It makes the system reach
        # the vicinnity of the equilibrium point very fast.
        # Other penalty parameters, like velovity, act as a damping factor,
        # preventing oscillations once the system is close to the target state.
        Q = [22.85374946834131, 4.173572355958551, 0.8160274195505297, 0.009991478547566969]
        R = 0.0008689413963011425

        A, B = linearize(GRAVITY, MASS_CART, MASS_POLE, LENGTH_POLE, MU_POLE)
        self.K, _, _ = control.lqr(A, B, np.eye(4) * np.array(Q), np.eye(1) * R)

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

        # These params have been found the same way as in Solution1.
        # We care about the position just enough not to hit the track ends,
        # but then we damp the divergence speed with the velocity penalty
        # to prevent any overshoot (which is just a waste of energy).
        Q = [11.474260126463925, 174.73857823578692, 0.2836756280323868, 0.006842520138545265]
        R = 0.06609290794456885

        A, B = linearize(GRAVITY, MASS_CART, MASS_POLE, LENGTH_POLE, MU_POLE)
        self.K, _, _ = control.lqr(A, B, np.eye(4) * np.array(Q), np.eye(1) * R)

    # Keep this signature unchanged for automated testing!
    # Returns one float - a desired force (u)
    def update(self, state):
        state = state.copy()
        state[0] -= self.target_pos
        return float(-self.K @ state)
