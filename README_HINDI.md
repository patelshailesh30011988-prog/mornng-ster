# Streamlit Morning Dashboard - Hindi README (Shailesh ke liye)

Yeh package aapko ek one-click web dashboard dega jo subah mobile/PC me khol ke market snapshot aur morning trade ideas dikhayega.

## Option A — ZIP download (sabse simple)
1) Is ZIP ko download karo aur extract karo.
2) Aapke pass agar GitHub account hai to repository banao aur extracted files ko upload karo (Add file -> Upload files).
3) Streamlit Community Cloud (https://streamlit.io/cloud) me login karke "New app" -> GitHub repo select karke deploy karo.
4) Ya agar aap nahi chahte GitHub to bhi: ZIP ki files ko manually GitHub me upload karna hoga kyunki Streamlit Cloud direct ZIP upload allow nahi karta.

## Option B — Git (advanced, agar aap comfortable ho)
1) Git install karo (windows: https://git-scm.com/downloads).
2) Terminal/Command Prompt me:
   ```bash
   git init
   git add .
   git commit -m "initial"
   git branch -M main
   git remote add origin https://github.com/yourusername/yourrepo.git
   git push -u origin main
   ```
3) Fir Streamlit Cloud pe deploy karo (select repo & file streamlit_app.py).

## Test locally (agar Python installed ho)
1) Python 3.10+ install karo.
2) Terminal me project folder open karke:
   ```bash
   pip install -r requirements.txt
   streamlit run streamlit_app.py
   ```
3) Browser khulega `http://localhost:8501` pe.

## Auto-refresh aur scheduling
- Streamlit app meta refresh use karta hai (AUTO_REFRESH_SECONDS variable). Page kholke rehta hai to har X second me refresh ho jayega.
- Agar aap chahte ho ki app khud roz 09:10 IST pe update ho kar Telegram pe bheje, to GitHub Actions + Telegram integration chahiye — mai isme madad kar dunga.

## Agar aap chahte ho:
- Main abhi ZIP bana ke upload kar du (download link du) — aap usko download karo aur Streamlit Cloud me upload kar do.
- Ya mai step-by-step GitHub+Streamlit deployment Hindi me likh du aur aap follow karo.

Batao, main ZIP bannake turant link de doon?