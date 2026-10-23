from pathlib import Path
import zipfile
root=Path(__file__).resolve().parent
files=['train.py','streamlit_app.py','requirements.txt','README.md','analysis.sql','run_sql.py','model.joblib','metrics.json','split.npz','INTERVIEW_GUIDE.md','EXPERIMENTS.md','SQL_RESULTS.txt','VALIDATION.json','validate.js','release.py']
with zipfile.ZipFile(root/'dist/project.zip','w',zipfile.ZIP_DEFLATED) as z:
    for f in files:
        z.write(root/f,f)
    for p in (root/'dist').iterdir():
        if p.is_file() and p.name!='project.zip':z.write(p,'dist/'+p.name)
print(root/'dist/project.zip')
