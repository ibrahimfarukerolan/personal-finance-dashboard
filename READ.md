# 💰 FinSight — Personal Finance Analytics Dashboard

FinSight is an interactive personal finance dashboard built with Python, Streamlit, Pandas, and Plotly.

The application helps users analyze their income, expenses, savings, and financial trends through interactive visualizations and automated insights.

## Features

- Upload financial transactions using CSV files
- Interactive date, category, and transaction type filters
- Income, expenses, and net savings calculations
- Savings rate and progress visualization
- Expense distribution donut chart
- Top spending categories analysis
- Monthly income vs expenses comparison
- Month-over-month spending trends
- Automated financial insights and summaries
- Transaction history and filtered CSV export
- Professional dark-themed interface

## Technologies

- Python 3.11
- Streamlit
- Pandas
- Plotly

## Dashboard Preview

![FinSight Dashboard](screenshots/dashboard.png)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/personal-finance-dashboard.git
cd personal-finance-dashboard
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

## CSV Format

Upload a CSV file with the following columns:

| Date | Category | Amount |
|------|----------|--------|
| 2026-10-01 | Salary | 5000 |
| 2026-10-02 | Rent | -1800 |
| 2026-10-03 | Groceries | -250 |

Positive amounts represent income, while negative amounts represent expenses.

A fictional sample dataset is included for demonstration purposes.

## Financial Analytics

FinSight calculates:

- **Total Income:** Sum of positive transactions
- **Total Expenses:** Absolute sum of negative transactions
- **Net Savings:** Income minus expenses
- **Savings Rate:** Net Savings / Total Income × 100
- **Monthly Spending Change:** Percentage change in expenses between consecutive months

Insights are descriptive and based on the selected transactions.

## Future Improvements

- PostgreSQL database integration
- User authentication
- Budget planning and spending limits
- Recurring transaction detection
- Additional financial forecasting features

## Privacy

Uploaded CSV data is processed by the Streamlit application. Do not upload sensitive financial data to an untrusted or publicly hosted instance.

## Author

Computer Science Student | Python | Data Analytics | Business Intelligence

## License

MIT License
```

**Important:** Replace `YOUR_USERNAME` with your actual GitHub username before publishing.

### 4. Create LICENSE

Create a file called `LICENSE`.

Paste:

```text
MIT License

Copyright (c) 2026 FinSight Contributors

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom
the Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall
be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
PURPOSE AND NONINFRINGEMENT.
```

You can replace `FinSight Contributors` with your name if you prefer.

### 5. Add a dashboard screenshot

In VS Code, create a folder named `screenshots`.

Open FinSight in Safari and upload your sample `transactions.csv`.

Take a screenshot of the main dashboard using `Command + Shift + 4`.

Save it inside `screenshots` with the exact filename:

`dashboard.png`

This will make your GitHub README display a preview of your application.

### 6. Check your final project structure

<box border radius="lg" padding={3} gap={2}>
  <row align=center gap={2}>
    <icon name="folder" color="secondary"/>
    **personal-finance-dashboard/**
  </row>
  <box padding={{left:4}} gap={2}>
    <row align=center gap={2}>
      <icon name="folder" color="secondary"/>
      .streamlit/
    </row>
    <row align=center gap={2} padding={{left:5}}>
      <icon name="file-code" color="secondary"/>
      config.toml
    </row>
    <row align=center gap={2}>
      <icon name="folder" color="secondary"/>
      screenshots/
    </row>
    <row align=center gap={2} padding={{left:5}}>
      <icon name="image" color="secondary"/>
      dashboard.png
    </row>
    {#each ["app.py","transactions.csv","requirements.txt",".gitignore","README.md","LICENSE"] as f}
      <row align=center gap={2}>
        <icon name="file" color="secondary"/>
        <text>{f}</text>
      </row>
    {/each}
    <row align=center gap={2}>
      <icon name="folder" color="secondary"/>
      <text color="secondary">.venv/ (local only)</text>
    </row>
  </box>
</box>

### 7. Verify the dependencies

Open your VS Code terminal and run:

```bash
python -m pip install -r requirements.txt
```

You should see that the packages are already installed.

Then run:

```bash
python -m streamlit run app.py
```

Check that FinSight still works.

---

### Your turn, bro!

Tell me **"Step 7 working"** when you've created all the files, saved your screenshot, and verified that the application runs.

Then we'll do **Step 8 — Publish FinSight on GitHub**, including the exact Git commands for your MacBook, and optionally deploy it so recruiters can open your dashboard directly in their browsers. 🚀