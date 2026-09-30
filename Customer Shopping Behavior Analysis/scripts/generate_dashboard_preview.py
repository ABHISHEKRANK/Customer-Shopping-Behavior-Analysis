"""
Generates reference dashboard layouts (PNG) from the cleaned dataset.

These images document the intended report design and populate the README.
Replace them with real Power BI screenshots once the .pbix is built.

Usage:  python scripts/generate_dashboard_preview.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "data" / "processed" / "customer_shopping_behavior_clean.csv")
OUT = ROOT / "images"
A = "Purchase Amount (USD)"

NAVY, TEAL, AMBER, CORAL, GREY, BG = "#1F3A5F", "#2A9D8F", "#E9C46A", "#E76F51", "#9CA3AF", "#F3F4F6"
plt.rcParams.update({"font.family": "DejaVu Sans", "axes.spines.top": False, "axes.spines.right": False})


def card(fig, x, y, w, h):
    fig.patches.append(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.002,rounding_size=0.008",
                                      transform=fig.transFigure, fc="white", ec="#E5E7EB", lw=1, zorder=-10))


def kpi(fig, x, y, w, h, label, value):
    card(fig, x, y, w, h)
    fig.text(x + w / 2, y + h * 0.62, value, ha="center", va="center", fontsize=20, fontweight="bold", color=NAVY)
    fig.text(x + w / 2, y + h * 0.20, label, ha="center", va="center", fontsize=9, color="#4B5563")


def panel(fig, rect, title):
    x, y, w, h = rect
    card(fig, x, y, w, h)
    fig.text(x + 0.012, y + h - 0.028, title, fontsize=10.5, fontweight="bold", color=NAVY)
    ax = fig.add_axes([x + 0.04, y + 0.05, w - 0.06, h - 0.13])
    ax.tick_params(labelsize=8, colors="#4B5563")
    return ax


def header(fig, title, subtitle):
    fig.patch.set_facecolor(BG)
    fig.patches.append(plt.Rectangle((0, 0.925), 1, 0.075, transform=fig.transFigure, fc=NAVY, zorder=-10))
    fig.text(0.02, 0.968, title, color="white", fontsize=16, fontweight="bold", va="center")
    fig.text(0.02, 0.940, subtitle, color="#CBD5E1", fontsize=8.5, va="center")
    fig.text(0.98, 0.955, "Reference layout | rendered from dataset", color="#CBD5E1", fontsize=8, ha="right", va="center")


def hbar(ax, s, color=NAVY, fmt="${:,.0f}"):
    s = s.sort_values()
    ax.barh(s.index, s.values, color=color, height=0.65)
    for i, v in enumerate(s.values):
        ax.text(v, i, " " + fmt.format(v), va="center", fontsize=7.5, color="#374151")
    ax.set_xticks([]); ax.spines["bottom"].set_visible(False); ax.spines["left"].set_color("#D1D5DB")


# ---------------------------- PAGE 1: Executive Overview ----------------------
fig = plt.figure(figsize=(16, 9))
header(fig, "Executive Overview", "Customer Shopping Behavior | 3,900 customers | 50 US states")
k = [("Total Revenue", f"${df[A].sum():,.0f}"), ("Customers", f"{df['Customer ID'].nunique():,}"),
     ("Avg Order Value", f"${df[A].mean():,.2f}"), ("Avg Rating", f"{df['Review Rating'].mean():.2f} / 5"),
     ("Subscriber Rate", f"{(df['Subscription Status'] == 'Yes').mean():.1%}"),
     ("Discount Usage", f"{(df['Discount Applied'] == 'Yes').mean():.1%}")]
for i, (l, v) in enumerate(k):
    kpi(fig, 0.02 + i * 0.1633, 0.80, 0.153, 0.105, l, v)

ax = panel(fig, (0.02, 0.42, 0.31, 0.36), "Revenue by Category")
c = df.groupby("Category")[A].sum().sort_values(ascending=False)
ax.pie(c, labels=[f"{n}\n{v / c.sum():.1%}" for n, v in c.items()], colors=[NAVY, TEAL, AMBER, CORAL],
       wedgeprops=dict(width=0.42, edgecolor="white"), textprops=dict(fontsize=8), startangle=90)

ax = panel(fig, (0.345, 0.42, 0.31, 0.36), "Revenue by Season")
s = df.groupby(["Season Sort", "Season"])[A].sum().reset_index()
b = ax.bar(s["Season"], s[A], color=[TEAL, AMBER, CORAL, NAVY], width=0.6)
for r in b:
    ax.text(r.get_x() + r.get_width() / 2, r.get_height(), f"${r.get_height() / 1000:.1f}K", ha="center", va="bottom", fontsize=8)
ax.set_yticks([]); ax.spines["left"].set_visible(False); ax.set_ylim(0, s[A].max() * 1.15)

ax = panel(fig, (0.67, 0.42, 0.31, 0.36), "Top 10 States by Revenue")
hbar(ax, df.groupby("Location")[A].sum().nlargest(10), TEAL)

ax = panel(fig, (0.02, 0.03, 0.47, 0.36), "Top 10 Items by Revenue")
hbar(ax, df.groupby("Item Purchased")[A].sum().nlargest(10), NAVY)

ax = panel(fig, (0.505, 0.03, 0.475, 0.36), "Average Order Value by Age Group")
g = df.groupby(["Age Group"])[A].mean()
b = ax.bar(g.index, g.values, color=NAVY, width=0.55)
for r in b:
    ax.text(r.get_x() + r.get_width() / 2, r.get_height(), f"${r.get_height():.2f}", ha="center", va="bottom", fontsize=8)
ax.set_yticks([]); ax.spines["left"].set_visible(False); ax.set_ylim(0, g.max() * 1.2)
fig.savefig(OUT / "dashboard_page1_executive_overview.png", dpi=130, facecolor=fig.get_facecolor())
plt.close(fig)

# ---------------------------- PAGE 2: Customer Insights -----------------------
fig = plt.figure(figsize=(16, 9))
header(fig, "Customer Insights", "Who our customers are, how loyal they are, and how they respond to offers")
sub = df.groupby("Subscription Status")[A].mean()
dis = df.groupby("Discount Applied")[A].mean()
k = [("Subscriber AOV", f"${sub['Yes']:.2f}"), ("Non-Subscriber AOV", f"${sub['No']:.2f}"),
     ("Discounted AOV", f"${dis['Yes']:.2f}"), ("Full-Price AOV", f"${dis['No']:.2f}"),
     ("Loyal Customers (41+)", f"{(df['Previous Purchases'] > 40).mean():.1%}"),
     ("Female Share", f"{(df['Gender'] == 'Female').mean():.1%}")]
for i, (l, v) in enumerate(k):
    kpi(fig, 0.02 + i * 0.1633, 0.80, 0.153, 0.105, l, v)

ax = panel(fig, (0.02, 0.42, 0.31, 0.36), "Customers by Age Group")
hbar(ax, df["Age Group"].value_counts().sort_index(ascending=False), NAVY, "{:,.0f}")

ax = panel(fig, (0.345, 0.42, 0.31, 0.36), "Customers by Loyalty Segment")
l = df.groupby(["Loyalty Sort", "Loyalty Segment"]).size().reset_index(name="n")
b = ax.bar(l["Loyalty Segment"].str.replace(" (", "\n(", regex=False), l["n"], color=TEAL, width=0.6)
for r in b:
    ax.text(r.get_x() + r.get_width() / 2, r.get_height(), f"{r.get_height():,.0f}", ha="center", va="bottom", fontsize=8)
ax.set_yticks([]); ax.spines["left"].set_visible(False); ax.set_ylim(0, l["n"].max() * 1.15)

ax = panel(fig, (0.67, 0.42, 0.31, 0.36), "Purchase Frequency")
f = df.groupby(["Frequency Sort", "Frequency Group"]).size().reset_index(name="n")
b = ax.bar(f["Frequency Group"], f["n"], color=AMBER, width=0.6)
for r in b:
    ax.text(r.get_x() + r.get_width() / 2, r.get_height(), f"{r.get_height():,.0f}", ha="center", va="bottom", fontsize=8)
ax.set_yticks([]); ax.spines["left"].set_visible(False); ax.tick_params(axis="x", labelsize=7.5)
ax.set_ylim(0, f["n"].max() * 1.15)

ax = panel(fig, (0.02, 0.03, 0.47, 0.36), "Subscription: Customers vs Revenue Share")
x = ["Customers", "Revenue"]
yes = [(df["Subscription Status"] == "Yes").mean(), df.loc[df["Subscription Status"] == "Yes", A].sum() / df[A].sum()]
ax.bar(x, [1, 1], color="#D1D5DB", width=0.5, label="Non-subscribers")
ax.bar(x, yes, color=NAVY, width=0.5, label="Subscribers")
for i, v in enumerate(yes):
    ax.text(i, v / 2, f"{v:.1%}", ha="center", color="white", fontsize=10, fontweight="bold")
ax.set_yticks([]); ax.spines["left"].set_visible(False); ax.set_ylim(0, 1.12); ax.legend(fontsize=8, frameon=False, loc="upper center", ncol=2)

ax = panel(fig, (0.505, 0.03, 0.475, 0.36), "Average Rating by Item (Bottom 8)")
hbar(ax, df.groupby("Item Purchased")["Review Rating"].mean().nsmallest(8), CORAL, "{:.2f}")
fig.savefig(OUT / "dashboard_page2_customer_insights.png", dpi=130, facecolor=fig.get_facecolor())
print("Saved previews to", OUT)
