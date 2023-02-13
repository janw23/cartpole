from cartpole_sim import main
import random
import multiprocessing as mp

NUM_GENERATIONS = 1000
POPULATION_SIZE = 32
# assert mp.cpu_count() * 4 == POPULATION_SIZE

# Q_init = [1, 1, 1, 1]
# R_init = 0.1

Q_init=[21.02211760811629, 3.9478084347877096, 0.7147666451729678, 0.11066171492165928]
R_init=0.0009347787056883676

Q_init=[21.999408980353664, 4.1172619425305825, 0.8001694255289518, 0.10301351202016129]
R_init=0.0008930899738592413

Q_init=[22.538540443282837, 4.1584448306171655, 0.8233448094466109, 0.09867107288915153]
R_init=0.0008838238455971222

Q_init=[22.56547882601147, 4.161064907879136, 0.8202020415219494, 0.09841635872461141]
R_init=0.0008792391803466091

Q_init=[22.56547882601147, 4.161064907879136, 0.8202020415219494, 0.01]
R_init=0.0008792391803466091

Q_init=[22.308012494127944, 4.180448969560065, 0.8382758708704124, 0.009841371162803574]
R_init=0.0008628919767630313

stddev = 0.1
stddev = 0.01
stddev = 0.001
stddev = 0.0001
stddev = 0.01

# search for best energy expenditure
Q_init=[22.308012494127944, 4.180448969560065, 0.8382758708704124, 0.009841371162803574]
R_init=10

Q_init=[17.291947344462805, 6.924063587554057, 0.6861077389998105, 0.00617776421869336]
R_init=7.691472172165687

Q_init=[100.56547882601147, 4.161064907879136, 0.8202020415219494, 0.01]
R_init=1

stddev = 0.1

def mutate(Q, R):
    new_Q = [q * (1 + random.gauss(0, stddev)) for q in Q]
    new_R = R * (1 + random.gauss(0, stddev))
    return new_Q, new_R

for gen in range(NUM_GENERATIONS):
    print(f"Generation {gen}")
    params = [(Q_init, R_init)] + [mutate(Q_init, R_init) for _ in range(POPULATION_SIZE - 1)]
    pool = mp.Pool(mp.cpu_count())
    results = pool.starmap(main, params)
    pool.close()
    pool.join()

    results = [(*res, Q, R) for res, (Q, R) in zip(results, params)]
    results = list(filter(lambda x: x[0] <= 0.05, results)) # Filter out failed tests
    results.sort(key=lambda x: x[1]) # Sort by average steps
    
    best = results[0]
    Q_init = best[2]
    R_init = best[3]

    print(f"Best: {best[0]} fail_frac, {best[1]} steps, Q={Q_init}, R={R_init}", flush=True)

