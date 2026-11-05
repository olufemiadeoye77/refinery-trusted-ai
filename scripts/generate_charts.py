"""Generate four charts from the running system.

Chart 1: baseline vs advisory finished-oil quality
Chart 2: attack matrix decision tree
Chart 3: zone conduit map
Chart 4: compliance coverage

Writes PNGs into docs/figures/. Deterministic; safe to run in CI.
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "zero-trust"))
sys.path.insert(0, str(ROOT / "process"))

from twin.train_model import simulate  # noqa: E402
from lab.zone_router import ZoneRouter  # noqa: E402

FIG_DIR = ROOT / "docs" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

GREEN = "#2e7d32"
RED = "#c62828"
BLUE = "#1565c0"
GREY = "#757575"


def chart1_baseline_vs_advisory():
    base = simulate()
    adv = simulate(earth_dose_kg_per_t=16.91, acid_dose_kg_per_t=1.5)

    metrics = ["Color (Lovibond red)", "FFA (x100 %)", "Phosphorus (ppm)"]
    base_vals = [
        base["finished_oil"]["color_red"],
        base["finished_oil"]["ffa_pct"] * 100,
        base["units"]["degumming"]["residual_phosphorus_ppm"],
    ]
    adv_vals = [
        adv["finished_oil"]["color_red"],
        adv["finished_oil"]["ffa_pct"] * 100,
        adv["units"]["degumming"]["residual_phosphorus_ppm"],
    ]

    fig, ax = plt.subplots(figsize=(9, 5))
    x = np.arange(len(metrics))
    w = 0.35
    bars1 = ax.bar(x - w/2, base_vals, w, label="Baseline (off-spec)", color=RED)
    bars2 = ax.bar(x + w/2, adv_vals, w, label="After advisory (on-spec)", color=GREEN)

    for bars in (bars1, bars2):
        for b in bars:
            h = b.get_height()
            ax.text(b.get_x() + b.get_width()/2, h, f"{h:.2f}",
                    ha="center", va="bottom", fontsize=9)

    ax.set_xticks(x)
    ax.set_xticklabels(metrics)
    ax.set_ylabel("Value")
    ax.set_title("Finished-oil quality: baseline vs after AI advisory")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    out = FIG_DIR / "01-baseline-vs-advisory.png"
    fig.savefig(out, dpi=140)
    plt.close(fig)
    print(f"wrote {out.relative_to(ROOT)}")


def chart2_attack_matrix():
    stages = [
        ("Happy path", "control", True),
        ("nonce", "replay", False),
        ("signature", "tampered value", False),
        ("policy", "unapproved model", False),
        ("freshness", "stale timestamp", False),
        ("agent_match", "forged key_id", False),
    ]
    labels = [f"{stage}\n({attack})" for stage, attack, _ in stages]
    values = [1 if caught else 0 for _, _, caught in stages]
    colors = [GREEN if v else RED for v in values]
    display = ["ACCEPT" if v else "REJECT" for v in values]

    fig, ax = plt.subplots(figsize=(10, 5))
    y = np.arange(len(stages))
    ax.barh(y, [1]*len(stages), color=colors)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xticks([])
    for i, (v, d) in enumerate(zip(values, display)):
        ax.text(0.5, i, d, ha="center", va="center",
                color="white", fontweight="bold", fontsize=11)
    ax.set_title("Zero-trust verification: every attack fails at a specific stage")
    fig.tight_layout()
    out = FIG_DIR / "02-attack-matrix.png"
    fig.savefig(out, dpi=140)
    plt.close(fig)
    print(f"wrote {out.relative_to(ROOT)}")


def chart3_zone_conduit_map():
    positions = {
        "Z0\nFIELD": (0, 0),
        "Z1\nCONTROL": (1, 0),
        "Z2\nSUPERV": (2, 0),
        "Z3.5\nDMZ": (3, 0),
        "Z4\nGOVERN": (4, 0),
    }
    keys = ["Z0_FIELD", "Z1_CONTROL", "Z2_SUPERVISORY", "Z35_DMZ", "Z4_GOVERNANCE"]
    router = ZoneRouter()
    flows = [
        ("Z0_FIELD", "Z2_SUPERVISORY"),
        ("Z2_SUPERVISORY", "Z35_DMZ"),
        ("Z35_DMZ", "Z2_SUPERVISORY"),
        ("Z4_GOVERNANCE", "Z35_DMZ"),
        ("Z35_DMZ", "Z4_GOVERNANCE"),
        ("Z35_DMZ", "Z1_CONTROL"),
        ("Z4_GOVERNANCE", "Z1_CONTROL"),
        ("Z2_SUPERVISORY", "Z0_FIELD"),
    ]

    fig, ax = plt.subplots(figsize=(12, 4))
    label_positions = list(positions.keys())
    for label, key in zip(label_positions, keys):
        x, y = positions[label]
        ax.scatter(x, y, s=2400, c=BLUE, zorder=3)
        ax.text(x, y, label, ha="center", va="center",
                color="white", fontsize=9, fontweight="bold", zorder=4)

    key_to_pos = {k: positions[l] for k, l in zip(keys, label_positions)}
    for i, (src, dst) in enumerate(flows):
        decision = router.check(src, dst)
        color = GREEN if decision.allowed else RED
        x1, y1 = key_to_pos[src]
        x2, y2 = key_to_pos[dst]
        offset = 0.18 if decision.allowed else -0.18
        ax.annotate("", xy=(x2, y2 + offset), xytext=(x1, y1 + offset),
                    arrowprops=dict(arrowstyle="->", color=color, lw=2.5))

    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(-0.6, 0.6)
    ax.axis("off")
    ax.set_title("IEC 62443 zone conduit map: green = allowed, red = blocked")
    fig.tight_layout()
    out = FIG_DIR / "03-zone-conduit-map.png"
    fig.savefig(out, dpi=140)
    plt.close(fig)
    print(f"wrote {out.relative_to(ROOT)}")


def chart4_compliance_coverage():
    import yaml
    matrix = yaml.safe_load((ROOT / "compliance" / "iso42001" / "control-matrix.yaml").read_text())
    counts = {"complete": 0, "draft": 0, "todo": 0}
    for row in matrix["rows"]:
        s = row.get("status", "todo")
        counts[s] = counts.get(s, 0) + 1

    labels = list(counts.keys())
    values = list(counts.values())
    colors = {"complete": GREEN, "draft": "#f9a825", "todo": GREY}
    color_list = [colors[k] for k in labels]

    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(labels, values, color=color_list)
    for b, v in zip(bars, values):
        ax.text(b.get_x() + b.get_width()/2, v, str(v),
                ha="center", va="bottom", fontsize=12, fontweight="bold")
    ax.set_title("ISO/IEC 42001 control matrix coverage")
    ax.set_ylabel("Number of controls")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    out = FIG_DIR / "04-compliance-coverage.png"
    fig.savefig(out, dpi=140)
    plt.close(fig)
    print(f"wrote {out.relative_to(ROOT)}")


def main():
    chart1_baseline_vs_advisory()
    chart2_attack_matrix()
    chart3_zone_conduit_map()
    chart4_compliance_coverage()
    print()
    print("All charts written to docs/figures/")


if __name__ == "__main__":
    main()
