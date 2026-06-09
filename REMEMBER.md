Fișier intern de notițe — lucruri de făcut când revenim la proiect

🔥 1. Activează GitHub Actions
Repo → Settings → Actions → General

Setează:

Allow all actions and reusable workflows

Read and write permissions

Fă un commit gol ca să pornească workflows:


git commit --allow-empty -m "Trigger Actions"
git push
🌱 2. Creează Branch Protection Rules
Pentru main:
Require pull request

Require status checks

Block direct pushes

Require linear history
Pentru dev:
Allow pushes

Optional: require PR pentru stabilitate

🌿 3. Stabilește Branching Strategy
main → stabil, gata de deploy

dev → integrare

feature/... → dezvoltare

fix/... → bugfix

hotfix/... → urgențe

🧹 4. Curățenie în workflows
Verifică .github/workflows/

Șterge ce nu mai folosim

Păstrează doar:

backend CI

frontend CI

security scan

code quality

📦 5. Adaugă README profesionist
Descriere proiect

Tech stack

Instrucțiuni de instalare

Structură repo

Cum rulezi backend + frontend

🔐 6. Finalizează ENV-urile
.env.development

.env.production

Variabile pentru frontend + backend

Documentează-le în README

🧪 7. Decide dacă păstrăm testele
Unit tests → ok

Integration tests → ok

🗂 8. Organizează structura repo-ului
/backend

/frontend

/docs

/infra (opțional)