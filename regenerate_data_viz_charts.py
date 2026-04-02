#!/usr/bin/env python3

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from bs4 import BeautifulSoup


BASE_DIR = Path("/home/tngai/data/Tutorials")
DATA_DIR = BASE_DIR / "data"
IMAGE_DIR = BASE_DIR / "assets" / "images"
INTERACTIVE_DIR = BASE_DIR / "assets" / "interactive"

MOMA_IMAGE_DIR = IMAGE_DIR / "moma"
MOMA_HTML_DIR = INTERACTIVE_DIR / "moma"
DATAVIZ_IMAGE_DIR = IMAGE_DIR / "data-viz"
DATAVIZ_HTML_DIR = INTERACTIVE_DIR / "data-viz"

MOMA_CSV_URL = "https://media.githubusercontent.com/media/MuseumofModernArt/collection/main/Artworks.csv"
MOMA_CSV_PATH = DATA_DIR / "Artworks.csv"

PAYROLL_URL = "https://www.seethroughny.net/tools/required/reports/payroll?action=get"
PAYROLL_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Origin": "https://www.seethroughny.net",
    "X-Requested-With": "XMLHttpRequest",
}


def ensure_dirs() -> None:
    for path in [
        DATA_DIR,
        MOMA_IMAGE_DIR,
        MOMA_HTML_DIR,
        DATAVIZ_IMAGE_DIR,
        DATAVIZ_HTML_DIR,
    ]:
        path.mkdir(parents=True, exist_ok=True)


def save_figure(
    fig: go.Figure,
    image_path: Path,
    html_path: Path,
    width: int = 1200,
    height: int = 700,
) -> None:
    fig.write_html(str(html_path), include_plotlyjs="cdn", full_html=True)
    fig.update_layout(width=width, height=height)
    fig.write_image(str(image_path), width=width, height=height, scale=2)


def save_table(df: pd.DataFrame, image_path: Path, html_path: Path, title: str) -> None:
    table = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=list(df.columns), align="left", fill_color="#d9e3f0"
                ),
                cells=dict(values=[df[col] for col in df.columns], align="left"),
            )
        ]
    )
    table.update_layout(title=title, margin=dict(l=20, r=20, t=60, b=20))
    save_figure(
        table, image_path, html_path, width=1200, height=max(400, 40 * len(df) + 120)
    )


def fetch_moma_csv() -> Path:
    if MOMA_CSV_PATH.exists() and MOMA_CSV_PATH.stat().st_size > 1000:
        return MOMA_CSV_PATH
    response = requests.get(MOMA_CSV_URL, timeout=120)
    response.raise_for_status()
    MOMA_CSV_PATH.write_bytes(response.content)
    return MOMA_CSV_PATH


def load_moma_dataframe() -> pd.DataFrame:
    csv_path = fetch_moma_csv()
    df = pd.read_csv(csv_path, low_memory=False)
    fill_columns = [
        "Artist",
        "Nationality",
        "BeginDate",
        "Gender",
        "Medium",
        "Date",
        "DateAcquired",
        "Classification",
        "Title",
    ]
    for column in fill_columns:
        if column in df.columns:
            df[column] = df[column].fillna("Unknown")
    return df


def build_moma_clean_dates(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df[
        df["DateAcquired"]
        .astype(str)
        .str.contains(r"^(?:\d{4}).*", regex=True, na=False)
        & df["Date"].astype(str).str.contains(r"^.*(?:\d{4}).*", regex=True, na=False)
    ].copy()
    cleaned["DateCreated"] = pd.to_numeric(
        cleaned["Date"].astype(str).str.extract(r"^.*(\d{4}).*")[0], errors="coerce"
    )
    cleaned["DateAcquiredFormatted"] = pd.to_numeric(
        cleaned["DateAcquired"].astype(str).str.extract(r"^(\d{4}).*")[0],
        errors="coerce",
    )
    cleaned = cleaned.dropna(subset=["DateCreated", "DateAcquiredFormatted"]).copy()
    cleaned = cleaned[cleaned["DateAcquiredFormatted"] >= 1700].copy()
    return cleaned


def generate_moma_charts() -> None:
    df = load_moma_dataframe()
    cleaned = build_moma_clean_dates(df)

    date_preview = df[["DateAcquired", "Date"]].head(12).copy()
    save_table(
        date_preview,
        MOMA_IMAGE_DIR / "moma-date-preview.png",
        MOMA_HTML_DIR / "moma-date-preview.html",
        "MoMA Date Columns Preview",
    )

    invalid_date_acquired = pd.DataFrame(
        {
            "Invalid DateAcquired Values": sorted(
                df.loc[
                    ~df["DateAcquired"]
                    .astype(str)
                    .str.contains(r"^(?:\d{4}).*", regex=True, na=False),
                    "DateAcquired",
                ]
                .astype(str)
                .dropna()
                .unique()
            )[:20]
        }
    )
    save_table(
        invalid_date_acquired,
        MOMA_IMAGE_DIR / "moma-dateacquired-invalid-values.png",
        MOMA_HTML_DIR / "moma-dateacquired-invalid-values.html",
        "MoMA Invalid DateAcquired Values",
    )

    medium_counts = cleaned["Medium"].value_counts().head(20).reset_index()
    medium_counts.columns = ["Medium", "Count"]
    save_table(
        medium_counts,
        MOMA_IMAGE_DIR / "moma-medium-counts-cleaned.png",
        MOMA_HTML_DIR / "moma-medium-counts-cleaned.html",
        "MoMA Medium Counts After Date Cleaning",
    )

    classification_counts = df["Classification"].value_counts().head(10).reset_index()
    classification_counts.columns = ["Classification", "Count"]
    save_table(
        classification_counts,
        MOMA_IMAGE_DIR / "moma-classification-top10.png",
        MOMA_HTML_DIR / "moma-classification-top10.html",
        "MoMA Top 10 Classifications",
    )

    arch_keywords = [
        "Mies van der Rohe Archive",
        "Architecture",
        "Frank Lloyd Wright Archive",
    ]
    arch = df[
        df["Classification"]
        .astype(str)
        .str.contains("|".join(map(re.escape, arch_keywords)), case=False, na=False)
    ].copy()
    arch = arch.dropna(subset=["Height (cm)", "Width (cm)"]).copy()
    arch["Height (cm)"] = pd.to_numeric(arch["Height (cm)"], errors="coerce")
    arch["Width (cm)"] = pd.to_numeric(arch["Width (cm)"], errors="coerce")
    arch = arch.dropna(subset=["Height (cm)", "Width (cm)"]).copy()
    arch = arch.head(1200).copy()

    arch_scatter = px.scatter(
        arch,
        x="Width (cm)",
        y="Height (cm)",
        hover_data=["Artist", "Title", "DateAcquired"],
        template="seaborn",
        title="MoMA Architecture Collection by Size",
    )
    save_figure(
        arch_scatter,
        MOMA_IMAGE_DIR / "moma-architecture-scatter.png",
        MOMA_HTML_DIR / "moma-architecture-scatter.html",
    )

    rects = []
    hovertext = []
    for _, row in arch.iterrows():
        hovertext.append(f"{row['Artist']}<br>{row['DateAcquired']}<br>{row['Title']}")
        rects.append(
            dict(
                type="rect",
                xref="x",
                yref="y",
                x0=0,
                y0=0,
                x1=row["Width (cm)"],
                y1=row["Height (cm)"],
                line=dict(color="rgb(200,200,200)", width=1),
                fillcolor="rgba(55,55,55,0.1)",
            )
        )
    arch_rectangles = go.Figure(
        data=[
            go.Scatter(
                x=arch["Width (cm)"].tolist(),
                y=arch["Height (cm)"].tolist(),
                mode="markers",
                text=hovertext,
                marker=dict(size=2, color="rgba(255,0,0,0.3)"),
            )
        ]
    )
    arch_rectangles.update_layout(
        title=f"MoMA Drawing Size<br><br>{len(arch)}",
        hovermode="closest",
        xaxis=dict(title="Width (cm)", ticklen=5, gridwidth=1),
        yaxis=dict(title="Height (cm)", ticklen=5, zeroline=True, gridwidth=1),
        shapes=rects,
        showlegend=False,
    )
    save_figure(
        arch_rectangles,
        MOMA_IMAGE_DIR / "moma-architecture-rectangles.png",
        MOMA_HTML_DIR / "moma-architecture-rectangles.html",
    )

    for medium, stem in [
        ("Oil on canvas", "moma-created-vs-acquired-oil-on-canvas"),
        ("Gelatin silver print", "moma-created-vs-acquired-gelatin-silver-print"),
    ]:
        subset = cleaned[cleaned["Medium"] == medium].copy()
        subset = subset.head(5000)
        fig = go.Figure(
            data=[
                go.Scatter(
                    x=subset["DateCreated"].tolist(),
                    y=subset["DateAcquiredFormatted"].tolist(),
                    mode="markers",
                    text=subset["Title"].tolist(),
                    marker=dict(size=10, color="rgba(200, 200, 200, .3)"),
                )
            ]
        )
        fig.update_layout(
            title=f"<b>MoMA Year Acquired VS Year Created</b><br>{medium}<br>{len(subset)}",
            hovermode="closest",
            xaxis=dict(title="Date Created", ticklen=5, gridwidth=2),
            yaxis=dict(title="Date Acquired", ticklen=5, zeroline=True, gridwidth=2),
            showlegend=False,
        )
        save_figure(fig, MOMA_IMAGE_DIR / f"{stem}.png", MOMA_HTML_DIR / f"{stem}.html")


def payroll_request(
    payload: list[tuple[str, str]],
    referer: str = "https://www.seethroughny.net/payrolls/",
) -> dict:
    headers = PAYROLL_HEADERS | {"Referer": referer}
    response = requests.post(PAYROLL_URL, headers=headers, data=payload, timeout=120)
    response.raise_for_status()
    return response.json()


def parse_payroll_rows(html: str) -> list[dict[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    rows = []
    for result_row in soup.find_all("tr", id=re.compile(r"^resultRow")):
        row_id = result_row.get("id", "").replace("resultRow", "")
        base_cells = [td.get_text(" ", strip=True) for td in result_row.find_all("td")]
        expand_row = soup.find("tr", id=f"expandRow{row_id}")
        details = {}
        if expand_row:
            for detail_row in expand_row.find_all("div", class_="row"):
                cols = detail_row.find_all("div")
                if len(cols) >= 2:
                    key = cols[0].get_text(" ", strip=True).replace(":", "")
                    value = cols[1].get_text(" ", strip=True)
                    details[key] = value
        rows.append(
            {
                "NAME": base_cells[1] if len(base_cells) > 1 else "",
                "SCHOOL": base_cells[2] if len(base_cells) > 2 else "",
                "SALARY": base_cells[3] if len(base_cells) > 3 else "",
                "TYPE": base_cells[4] if len(base_cells) > 4 else "",
                "DEPARTMENT": details.get("SubAgency/Type", ""),
                "TITLE": details.get("Title", ""),
                "RATE OF PAY": details.get("Rate of Pay", ""),
                "PAY YEAR": details.get("Pay Year", ""),
                "PAY BASIS": details.get("Pay Basis", ""),
                "BRANCH": details.get("Branch/Major Category", ""),
            }
        )
    return rows


def fetch_payroll_pages(
    initial_payload: list[tuple[str, str]], referer: str
) -> pd.DataFrame:
    first = payroll_request(initial_payload, referer=referer)
    rows = parse_payroll_rows(first["html"])
    result_id = str(first["result_id"])
    total_pages = int(first["total_pages"])

    for page in range(2, total_pages + 1):
        payload = initial_payload + [
            ("result_id", result_id),
            ("current_page", str(page)),
        ]
        result = payroll_request(payload, referer=referer)
        rows.extend(parse_payroll_rows(result["html"]))

    df = pd.DataFrame(rows)
    df["SALARY_NUMERIC"] = (
        df["SALARY"]
        .astype(str)
        .str.replace(r"[^0-9.-]", "", regex=True)
        .replace("", pd.NA)
        .astype(float)
    )
    return df


def generate_salary_charts() -> None:
    fit_df = fetch_payroll_pages(
        [("url", PAYROLL_URL), ("nav_request", "0"), ("result_id", "107209525")],
        referer="https://www.seethroughny.net/payrolls/107209525",
    )

    fit_simple = go.Figure(
        data=[go.Box(name="FIT", y=fit_df["SALARY_NUMERIC"].dropna())]
    )
    fit_simple.update_layout(title="FIT Faculty Salary")
    save_figure(
        fit_simple,
        DATAVIZ_IMAGE_DIR / "fit-faculty-salary-box.png",
        DATAVIZ_HTML_DIR / "fit-faculty-salary-box.html",
    )

    fit_points = go.Figure(
        data=[
            go.Box(
                name="FIT",
                y=fit_df["SALARY_NUMERIC"].dropna(),
                boxpoints="all",
                jitter=0.2,
                pointpos=-1.5,
            )
        ]
    )
    fit_points.update_layout(title="FIT Faculty Salary")
    save_figure(
        fit_points,
        DATAVIZ_IMAGE_DIR / "fit-faculty-salary-box-all-points.png",
        DATAVIZ_HTML_DIR / "fit-faculty-salary-box-all-points.html",
    )

    city_payload = [
        ("url", PAYROLL_URL),
        ("nav_request", "0"),
        ("PayYear[]", "2018"),
        ("AgencyName[]", "CUNY"),
        ("SubAgencyName[]", "City College"),
        ("SubAgencyName[]", "City College Adjunct"),
        ("SubAgencyName[]", "City College EH"),
        ("SubAgencyName[]", "City College Hourly"),
        ("SubAgencyName[]", "City College Lag"),
        ("SortBy", "YTDPay DESC"),
    ]
    city_df = fetch_payroll_pages(
        city_payload, referer="https://www.seethroughny.net/payrolls/"
    )
    city_prof = city_df[
        city_df["TITLE"].astype(str).str.contains(r"Prof|Lect", case=False, na=False)
    ].copy()
    title_order = city_prof["TITLE"].value_counts().head(12).index.tolist()
    traces = []
    for title in title_order:
        subset = city_prof.loc[city_prof["TITLE"] == title, "SALARY_NUMERIC"].dropna()
        traces.append(
            go.Box(
                name=title,
                y=subset,
                boxpoints="all",
                jitter=0.3,
                pointpos=-1.8,
            )
        )
    city_fig = go.Figure(data=traces)
    city_fig.update_layout(title="City College Faculty Salary")
    save_figure(
        city_fig,
        DATAVIZ_IMAGE_DIR / "city-college-faculty-salary-box.png",
        DATAVIZ_HTML_DIR / "city-college-faculty-salary-box.html",
        width=1600,
        height=800,
    )


def main() -> None:
    ensure_dirs()
    generate_moma_charts()
    generate_salary_charts()
    print("Regenerated local chart outputs.")


if __name__ == "__main__":
    main()
