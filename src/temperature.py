import numpy as np


def temperatureProfile(TEMP_PROFILE, T0, TEMPERATURE_LADDER, ITERATIONS):
    if TEMP_PROFILE == "lin":
        return mkCoolingScheduleLin(T0,TEMPERATURE_LADDER,ITERATIONS)
    elif TEMP_PROFILE == "bilin":
        return mkCoolingScheduleBilin(T0,TEMPERATURE_LADDER,ITERATIONS,0.9*T0,0.1*T0,0.2,0.8)
    elif TEMP_PROFILE == "exp":
        return mkCoolingScheduleExp(T0,TEMPERATURE_LADDER,ITERATIONS,0.1*T0)
    else:
        print("Invalid temperature profile. Exiting...")
        exit(1)

def mkCoolingScheduleLin(T0,K,iter):
    T = np.ones(iter)*T0
    dT = T0/(iter/K)
    for k in np.arange(2,iter):
        T[k] = T[k-1]
        if k%K == 0:
            T[k] -= dT
    return T

def mkCoolingScheduleBilin(T0,K,iter,T1,T2,anteil1,anteil2):
    T = np.ones(iter)*T0;

    k1 = iter * (anteil1/1)
    k2 = iter * (anteil2/1)

    for k in np.arange(2,iter):
        T[k] = T[k-1]
        dT = 0

        if k%K == 0:
            if k<k1:
                dT = -(T1-T0)/(k1- 0)*K
            elif k<k2:
                dT = -(T2-T1)/(k2-k1)*K
            else:
                dT = -(0 -T2)/(iter-k2)*K

            T[k] -= dT

        if T[k]<0:
            T[k]=0

    return T

def mkCoolingScheduleExp(T0,K,iter,Te):
    T = np.ones(iter)*T0;

    λ = -1/iter * np.log(Te/T0)

    for k in np.arange(2,iter):
        T[k] = T[k-1]

        if k%K == 0:
            T[k] = T0 * np.exp(-λ*k)

    return T