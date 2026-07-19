"""
visualization.py
================
Reusable plotting functions for the Ethiopia Financial Inclusion project.
All functions return Matplotlib Figure objects so callers can save or
display them as needed.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import numpy as np
from typing import Optional


# ---------------------------------------------------------------------------
# Style defaults
# ---------------------------------------------------------------------------

PILLAR_COLORS = {
    "ACCESS": "#2196F3",
    "USAGE": "#4CAF50",
    "GENDER": "#E91E63",
    "AFFORDABILITY": "#FF9800",
    "QUALITY": "#9C27B0",
    "TRUST": "#00BCD4",
    "DEPTH": "#795548",
}

DEFAULT_FIGSIZE = (12, 6)


def _style_axes(ax: plt.Axes, title: str, xlabel: str = "", ylabel: str = "") -> None:
    """Apply consistent styling to an axes object."""
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=11)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=11)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.tick_params(labelsize=10)


# ---------------------------------------------------------------------------
# Dataset overview charts
# ---------------------------------------------------------------------------

def plot_record_type_distribution(df: pd.DataFrame) -> plt.Figure:
    """Bar chart of records by record_type."""
    counts = df["record_type"].value_counts()
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(counts.index, counts.values, color=["#2196F3", "#4CAF50", "#FF9800", "#9C27B0"])
    ax.bar_label(bars, padding=3, fontsize=11, fontweight="bold")
    _style_axes(ax, "Records by Type", "Record Type", "Count")
    fig.tight_layout()
    return fig


def plot_pillar_distribution(df: pd.DataFrame) -> plt.Figure:
    """Horizontal bar chart of records by pillar."""
    pillar_df = df[df["pillar"].notna() & (df["pillar"] != "")]
    counts = pillar_df["pillar"].value_counts()
    colors = [PILLAR_COLORS.get(p, "#607D8B") for p in counts.index]
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(counts.index, counts.values, color=colors)
    ax.bar_label(bars, padding=3, fontsize=11, fontweight="bold")
    _style_axes(ax, "Records by Pillar (observations, targets & impact links)", "Count")
    ax.invert_yaxis()
    fig.tight_layout()
    return fig


def plot_confidence_distribution(df: pd.DataFrame) -> plt.Figure:
    """Pie chart of confidence level distribution."""
    counts = df["confidence"].value_counts()
    colors = {"high": "#4CAF50", "medium": "#FF9800", "low": "#F44336", "estimated": "#9E9E9E"}
    clrs = [colors.get(c, "#607D8B") for c in counts.index]
    fig, ax = plt.subplots(figsize=(7, 5))
    wedges, texts, autotexts = ax.pie(
        counts.values, labels=counts.index, autopct="%1.0f%%",
        colors=clrs, startangle=90, textprops={"fontsize": 11},
    )
    for at in autotexts:
        at.set_fontweight("bold")
    ax.set_title("Data Confidence Level Distribution", fontsize=14, fontweight="bold", pad=12)
    fig.tight_layout()
    return fig


def plot_source_type_distribution(df: pd.DataFrame) -> plt.Figure:
    """Bar chart of source type counts."""
    counts = df["source_type"].value_counts()
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(counts.index, counts.values, color="#5C6BC0")
    ax.bar_label(bars, padding=3, fontsize=10, fontweight="bold")
    _style_axes(ax, "Records by Source Type", "Source Type", "Count")
    plt.xticks(rotation=30, ha="right")
    fig.tight_layout()
    return fig


def plot_temporal_coverage(df: pd.DataFrame) -> plt.Figure:
    """Scatter plot showing temporal coverage by indicator."""
    obs = df[df["record_type"] == "observation"].copy()
    obs["observation_date"] = pd.to_datetime(obs["observation_date"], errors="coerce")
    obs = obs.dropna(subset=["observation_date", "indicator_code"])

    fig, ax = plt.subplots(figsize=(14, 7))
    indicators = obs["indicator_code"].unique()
    y_pos = {ind: i for i, ind in enumerate(sorted(indicators))}
    colors = [PILLAR_COLORS.get(p, "#607D8B") for p in
              obs.drop_duplicates("indicator_code")
                  .set_index("indicator_code")["pillar"]
                  .reindex(sorted(indicators))
                  .values]

    for _, row in obs.iterrows():
        ind = row["indicator_code"]
        ax.scatter(row["observation_date"], y_pos[ind],
                   s=80, color=PILLAR_COLORS.get(row.get("pillar", ""), "#607D8B"),
                   alpha=0.85, zorder=3)

    ax.set_yticks(list(y_pos.values()))
    ax.set_yticklabels(list(y_pos.keys()), fontsize=9)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.xaxis.set_major_locator(mdates.YearLocator(2))
    _style_axes(ax, "Temporal Coverage by Indicator", "Year", "Indicator Code")
    ax.grid(axis="x", linestyle="--", alpha=0.3)

    # Legend for pillars
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=c, label=p) for p, c in PILLAR_COLORS.items()]
    ax.legend(handles=legend_elements, loc="lower right", fontsize=9, framealpha=0.8)

    fig.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# Access analysis charts
# ---------------------------------------------------------------------------

def plot_account_ownership_trajectory(df: pd.DataFrame) -> plt.Figure:
    """Line chart of account ownership rate 2011-2024 (all genders)."""
    obs = df[
        (df["record_type"] == "observation") &
        (df["indicator_code"] == "ACC_OWNERSHIP") &
        (df["gender"].isin(["all", float("nan")]))
    ].copy()
    obs["observation_date"] = pd.to_datetime(obs["observation_date"], errors="coerce")
    obs["value_numeric"] = pd.to_numeric(obs["value_numeric"], errors="coerce")
    obs = obs.dropna(subset=["observation_date", "value_numeric"])
    obs = obs[obs["gender"].fillna("all") == "all"].sort_values("observation_date")

    fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)
    ax.plot(obs["observation_date"], obs["value_numeric"],
            "o-", color="#2196F3", linewidth=2.5, markersize=9, zorder=4, label="Account Ownership (%)")

    for _, row in obs.iterrows():
        ax.annotate(f"{row['value_numeric']:.0f}%",
                    xy=(row["observation_date"], row["value_numeric"]),
                    xytext=(0, 12), textcoords="offset points",
                    ha="center", fontsize=10, fontweight="bold", color="#1565C0")

    # Add target line if present
    targets = df[
        (df["record_type"] == "target") &
        (df["indicator_code"] == "ACC_OWNERSHIP")
    ].copy()
    targets["observation_date"] = pd.to_datetime(targets["observation_date"], errors="coerce")
    targets["value_numeric"] = pd.to_numeric(targets["value_numeric"], errors="coerce")
    if not targets.empty:
        ax.scatter(targets["observation_date"], targets["value_numeric"],
                   s=120, marker="*", color="#FF9800", zorder=5, label="NFIS-II Target")

    ax.set_ylim(0, 100)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=100))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    _style_axes(ax, "Ethiopia Account Ownership Rate Trajectory (2014–2024)",
                "Year", "Adults with an Account (%)")
    ax.legend(fontsize=10)
    ax.set_facecolor("#F8FBFF")
    fig.tight_layout()
    return fig


def plot_gender_gap(df: pd.DataFrame) -> plt.Figure:
    """Grouped bar chart of account ownership by gender across survey years."""
    obs = df[
        (df["record_type"] == "observation") &
        (df["indicator_code"] == "ACC_OWNERSHIP")
    ].copy()
    obs["observation_date"] = pd.to_datetime(obs["observation_date"], errors="coerce")
    obs["value_numeric"] = pd.to_numeric(obs["value_numeric"], errors="coerce")
    obs = obs.dropna(subset=["observation_date", "value_numeric"])
    obs["year"] = obs["observation_date"].dt.year

    pivot = obs.pivot_table(index="year", columns="gender", values="value_numeric", aggfunc="mean")
    pivot = pivot[[c for c in ["all", "male", "female"] if c in pivot.columns]]

    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(pivot.index))
    width = 0.25
    gender_colors = {"all": "#2196F3", "male": "#1976D2", "female": "#E91E63"}
    for i, (col, clr) in enumerate(gender_colors.items()):
        if col in pivot.columns:
            bars = ax.bar(x + i * width, pivot[col], width, label=col.title(), color=clr, alpha=0.85)
            ax.bar_label(bars, fmt="%.0f%%", padding=2, fontsize=9)

    ax.set_xticks(x + width)
    ax.set_xticklabels(pivot.index)
    ax.set_ylim(0, 80)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=100))
    _style_axes(ax, "Account Ownership by Gender (Survey Years)", "Year", "Adults with an Account (%)")
    ax.legend(fontsize=10)
    fig.tight_layout()
    return fig


def plot_mobile_money_penetration(df: pd.DataFrame) -> plt.Figure:
    """Line chart of mobile money account rate trend."""
    obs = df[
        (df["record_type"] == "observation") &
        (df["indicator_code"] == "ACC_MM_ACCOUNT") &
        (df["gender"].fillna("all") == "all")
    ].copy()
    obs["observation_date"] = pd.to_datetime(obs["observation_date"], errors="coerce")
    obs["value_numeric"] = pd.to_numeric(obs["value_numeric"], errors="coerce")
    obs = obs.dropna(subset=["observation_date", "value_numeric"]).sort_values("observation_date")

    fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)
    ax.plot(obs["observation_date"], obs["value_numeric"],
            "s-", color="#4CAF50", linewidth=2.5, markersize=9, label="Mobile Money Account Rate (%)")

    for _, row in obs.iterrows():
        ax.annotate(f"{row['value_numeric']:.1f}%",
                    xy=(row["observation_date"], row["value_numeric"]),
                    xytext=(0, 12), textcoords="offset points",
                    ha="center", fontsize=10, fontweight="bold", color="#2E7D32")

    ax.set_ylim(0, 30)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=100))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    _style_axes(ax, "Mobile Money Account Penetration in Ethiopia",
                "Year", "Adults with Mobile Money Account (%)")
    ax.legend(fontsize=10)
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# Event timeline chart
# ---------------------------------------------------------------------------

def plot_event_timeline(df: pd.DataFrame, indicator_code: str = "ACC_OWNERSHIP") -> plt.Figure:
    """Overlay events on an indicator trend chart.

    Parameters
    ----------
    df : pd.DataFrame
        Full unified dataset.
    indicator_code : str
        The indicator to plot as the background trend line.
    """
    obs = df[
        (df["record_type"] == "observation") &
        (df["indicator_code"] == indicator_code) &
        (df["gender"].fillna("all") == "all")
    ].copy()
    obs["observation_date"] = pd.to_datetime(obs["observation_date"], errors="coerce")
    obs["value_numeric"] = pd.to_numeric(obs["value_numeric"], errors="coerce")
    obs = obs.dropna(subset=["observation_date", "value_numeric"]).sort_values("observation_date")

    events = df[df["record_type"] == "event"].copy()
    events["observation_date"] = pd.to_datetime(events["observation_date"], errors="coerce")
    events = events.dropna(subset=["observation_date"]).sort_values("observation_date")

    fig, ax = plt.subplots(figsize=(14, 7))

    # Trend line
    if not obs.empty:
        ax.plot(obs["observation_date"], obs["value_numeric"],
                "o-", color="#2196F3", linewidth=2.5, markersize=9, zorder=4, label=indicator_code)
        ax.set_ylim(0, max(obs["value_numeric"].max() * 1.3, 80))
        ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=100))

    # Event markers
    cat_colors = {
        "product_launch": "#E53935", "market_entry": "#8E24AA",
        "market_exit": "#757575", "policy": "#1E88E5",
        "regulation": "#00ACC1", "infrastructure": "#43A047",
        "partnership": "#FB8C00", "milestone": "#FDD835",
        "economic": "#6D4C41", "pricing": "#F48FB1",
    }
    y_vals = obs["value_numeric"].tolist() if not obs.empty else [50]
    y_min, y_max = min(y_vals) * 0.7, max(y_vals) * 1.25

    for i, (_, ev) in enumerate(events.iterrows()):
        clr = cat_colors.get(ev.get("category", ""), "#78909C")
        ax.axvline(ev["observation_date"], color=clr, linewidth=1.5, alpha=0.6, linestyle="--")
        ypos = y_max * (0.92 - (i % 5) * 0.08)
        short_name = str(ev.get("indicator", ""))[:22]
        ax.text(ev["observation_date"], ypos, short_name,
                rotation=45, ha="left", va="top", fontsize=7.5, color=clr, fontweight="bold")

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7]))
    plt.xticks(rotation=30, ha="right")

    # Event category legend
    from matplotlib.lines import Line2D
    legend_lines = [
        Line2D([0], [0], color=c, linewidth=2, linestyle="--", label=cat)
        for cat, c in cat_colors.items()
        if cat in events["category"].values
    ]
    ax.legend(handles=legend_lines, loc="upper left", fontsize=8, framealpha=0.85,
              title="Event Category", title_fontsize=9)

    _style_axes(ax, f"Event Timeline overlaid on {indicator_code} Trend",
                "Date", "Value")
    fig.tight_layout()
    return fig
