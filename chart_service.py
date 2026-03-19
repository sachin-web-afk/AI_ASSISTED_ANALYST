def generate_chart(question, data):

    if not data:
        return None

    rows = data.get("rows")

    if not rows or len(rows) < 2:
        return None

    # convert rows safely
    clean_rows = []
    for r in rows:
        try:
            clean_rows.append(r.asDict())
        except:
            clean_rows.append(dict(r))

    q = question.lower()
    sample = clean_rows[0]

    text_col = None

    # detect text column
    for k, v in sample.items():
        if isinstance(v, str):
            text_col = k
            break

    if not text_col:
        return None

    # 🎯 PRIORITY METRICS (smart ranking)
    priority_metrics = [
        "Employment_Rate",
        "Research_Impact_Score",
        "Intl_Student_Ratio",
        "National_Rank"
    ]

    numeric_col = None

    # ✅ STEP 1: detect from question intent
    if "employment" in q:
        numeric_col = "Employment_Rate"
    elif "research" in q:
        numeric_col = "Research_Impact_Score"
    elif "international" in q:
        numeric_col = "Intl_Student_Ratio"
    elif "rank" in q:
        numeric_col = "National_Rank"

    # ✅ STEP 2: fallback → best available metric
    if not numeric_col:
        for col in priority_metrics:
            if col in sample:
                numeric_col = col
                break

    if not numeric_col:
        return None

    # build values
    values = []
    for r in clean_rows:
        values.append({
            text_col: r[text_col],
            numeric_col: r[numeric_col]
        })

    # 🎯 SMART CHART TYPE
    if "trend" in q or "year" in q:
        mark = "line"
    elif "compare" in q or len(values) <= 10:
        mark = "bar"
    else:
        mark = "bar"

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "width": 600,
        "height": 400,
        "data": {"values": values},
        "mark": {"type": mark, "tooltip": True},
        "encoding": {
            "x": {
                "field": text_col,
                "type": "nominal",
                "axis": {"labelAngle": -30}
            },
            "y": {
                "field": numeric_col,
                "type": "quantitative"
            }
        }
    }