Command Line code

cd "C:\Users\Ty\Documents\Chicago\MLOps\Assignment 1"

git init
dvc init -f

mkdir "C:\Users\Ty\Documents\Chicago\MLOps\Assignment 1\dvc-remote"
dvc remote add -d myremote "C:\Users\Ty\Documents\Chicago\MLOps\Assignment 1\dvc-remote"

dvc add v1.csv

git add v1.csv.dvc .gitignore


git commit -m "feat: Add and version baseline dataset v1"


git tag -a v1.0 -m "Baseline model with v1 raw data"


dvc push



dvc add v2.csv


git add v2.csv.dvc


git commit -m "feat: Add and version cleaned dataset v2"


git tag -a v2.0 -m "Improved model with v2 cleaned data"


dvc push

to switch 

git checkout v1.0
dvc pull
dvc checkout

git checkout v2.0
dvc pull
dvc checkout