# app/compute.py
from __future__ import annotations

import numpy as np
from pandas import DataFrame
from scipy import interpolate

from .tables import (
    DB,
    CNW,
    CNL,
    CNgamma90,
    CNccZ1,
    CNccZ2,
    CNccZ3,
    KZT_TABLE1,
    KZT_TABLE2,
)
from .schemas import (
    SolveRequest,
    SolveResponse,
    BasisOut,
    MainOut,
    CCZoneOut,
)


def _fundamental_frequency(h_ft: float, structural_type: str) -> float:
    """ASCE 계통에서 사용한 경험식 그대로."""
    if structural_type == "Steel":
        return 22.2 / (h_ft**0.8)
    if structural_type == "Concrete":
        return 43.5 / (h_ft**0.9)
    return 75.0 / h_ft


def _interp(df: DataFrame, xcol: str, ycol: str, xval: float) -> float:
    f = interpolate.interp1d(df[xcol], df[ycol], kind="linear")
    return float(f(xval))


def solve(req: SolveRequest) -> SolveResponse:
    # ---------- Effective Wind Area / zone a / EWA ----------
    eff_area = max(req.purlin_s * req.purlin_l, (req.purlin_l**2) / 3)
    zone_a = max(
        min(req.B * 0.1, req.L * 0.1, 0.4 * req.h), 0.04 * min(req.B, req.L), 0.9
    )
    if eff_area <= zone_a**2:
        ewa = "EWA1"
    elif eff_area <= 4 * (zone_a**2):
        ewa = "EWA2"
    else:
        ewa = "EWA3"

    # ---------- Fundamental freq / Gust factor ----------
    H_ft = req.h / 0.305
    na = _fundamental_frequency(H_ft, req.structural_type)

    exp_db = DB[req.exp]
    z_bar = max(req.h * 0.6, exp_db["z_min"])
    gq = 3.4
    gv = 3.4

    Lz = exp_db["l"] * (z_bar / 10) ** (exp_db["epsilon"])
    Q = (1 / (1 + 0.63 * ((req.B + req.h) / Lz) ** 0.63)) ** 0.5
    Vz = exp_db["b"] * (z_bar / 10) ** (exp_db["alpha_bar"]) * req.V
    N1 = na * Lz / Vz
    Rn = 7.47 * N1 / ((1 + 10.3 * N1) ** (5 / 3))

    eta1 = 4.6 * na * req.h / Vz
    eta2 = 4.6 * na * req.B / Vz
    eta3 = 15.4 * na * req.L / Vz

    econst = np.e
    Rh = 1 / eta1 - 1 / (2 * eta1**2) * (1 - econst ** (-2 * eta1))
    RB = 1 / eta2 - 1 / (2 * eta2**2) * (1 - econst ** (-2 * eta2))
    RL = 1 / eta3 - 1 / (2 * eta3**2) * (1 - econst ** (-2 * eta3))

    R = (1 / req.beta * Rn * Rh * RB * (0.53 + 0.479 * RL)) ** 0.5
    Iz = exp_db["c"] * (10 / z_bar) ** (1 / 6)
    gR = (2 * np.log(3600 * na)) ** 0.5 + 0.577 / (2 * (np.log(3600 * na)) ** 0.5)

    if na >= 1:
        G = 0.925 * ((1 + 1.7 * gq * Iz * Q) / (1 + 1.7 * gv * Iz))
    else:
        G = 0.925 * (
            (1 + 1.7 * Iz * (gq**2 * Q**2 + gR**2 * R**2) ** 0.5) / (1 + 1.7 * gv * Iz)
        )

    # ---------- Kz ----------
    if req.h > 4.572:
        Kz = round(2.01 * (req.h / exp_db["z_g"]) ** (2 / exp_db["alpha"]), 4)
    else:
        Kz = round(2.01 * (4.572 / exp_db["z_g"]) ** (2 / exp_db["alpha"]), 4)

    # ---------- Kzt (지형 영향) ----------
    if req.topographic.enabled:
        ratio = req.topographic.H_hill / req.topographic.Lh
        k1_base = KZT_TABLE1[req.exp][req.topographic.topho]
        K1 = k1_base * (0.5 if ratio > 0.5 else ratio)

        K2 = 1 - abs(req.topographic.x) / (
            KZT_TABLE2["mus"][req.topographic.topho + req.topographic.UD]
            * req.topographic.Lh
        )
        k3 = float(
            np.e
            ** (
                -KZT_TABLE2["gammas"][req.topographic.topho]
                * req.h
                / req.topographic.Lh
            )
        )
        Kzt = round((1 + K1 * K2 * k3) ** 2, 4)
    else:
        Kzt = 1.0

    # 공통 동압 (Pa) – Kd, V 포함
    q0 = 0.613 * Kz * Kzt * req.Kd * (req.V**2)

    # ---------- CNW / CNL (보간) ----------
    LoadCase = ["A", "B"]
    gammas = ["gamma0", "gamma180"]

    df_cnw = DataFrame(CNW)
    df_cnl = DataFrame(CNL)
    df_g90 = DataFrame(CNgamma90)

    cnw_vals: list[float] = []
    for i in LoadCase:
        for j in gammas:
            key = f"{req.Type}{i}{j}{req.blockage}"
            cnw_vals.append(round(_interp(df_cnw, "RoofSlop", key, req.x_deg), 5))

    cnl_vals: list[float] = []
    for i in LoadCase:
        for j in gammas:
            key = f"{req.Type}{i}{j}{req.blockage}"
            cnl_vals.append(round(_interp(df_cnl, "RoofSlop", key, req.x_deg), 5))

    gamma90_keys = ["gamma90<h", "gamma90<2h", "gamma90>2h"]
    cng90_vals: list[float] = []
    for i in LoadCase:
        for j in gamma90_keys:
            key = f"{req.Type}{i}{j}{req.blockage}"
            cng90_vals.append(round(_interp(df_g90, "RoofSlop", key, req.x_deg), 5))

    # ---------- Main pressures ----------
    PW_Main = [round(q0 * G * c, 1) for c in cnw_vals]
    PL_Main = [round(q0 * G * c, 1) for c in cnl_vals]
    Pgamma90_Main = [round(q0 * G * c, 1) for c in cng90_vals]

    # ---------- C&C (Z3, Z2, Z1) ----------
    ewa_tag = ewa  # "EWA1" / "EWA2" / "EWA3"
    cc_tables = [(3, DataFrame(CNccZ3)), (2, DataFrame(CNccZ2)), (1, DataFrame(CNccZ1))]

    cc_out: list[CCZoneOut] = []
    for zone, df in cc_tables:
        keyA = f"{req.Type}{ewa_tag}{req.blockage}A"
        keyB = f"{req.Type}{ewa_tag}{req.blockage}B"
        CNcc_A = float(_interp(df, "RoofSlop", keyA, req.x_deg))
        CNcc_B = float(_interp(df, "RoofSlop", keyB, req.x_deg))
        P_A = round(q0 * G * CNcc_A, 1)
        P_B = round(q0 * G * CNcc_B, 1)
        cc_out.append(
            CCZoneOut(
                zone=zone,
                CNcc_A=round(CNcc_A, 4),
                CNcc_B=round(CNcc_B, 4),
                Pcc_A_Pa=P_A,
                Pcc_B_Pa=P_B,
            )
        )

    return SolveResponse(
        basis=BasisOut(
            EffecWindArea=eff_area,
            zone_a=zone_a,
            EWA=ewa,
            na=round(na, 4),
            G=round(G, 4),
            Kz=Kz,
            Kzt=Kzt,
        ),
        main=MainOut(
            CNW=cnw_vals,
            CNL=cnl_vals,
            CNgamma90=cng90_vals,
            PW_Main=PW_Main,
            PL_Main=PL_Main,
            Pgamma90_Main=Pgamma90_Main,
        ),
        cc=cc_out,
    )
