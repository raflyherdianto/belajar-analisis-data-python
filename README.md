# Dashboard Bike Sharing Streamlit
Untuk menjalankan dashboard ini di local ada beberapa langkah yang perlu dilakukan

## Install Dependencies
Sesuaikan dengan environment di komputer apakah menggunakan Anaconda atau Pipenv

### Setup Environment - Anaconda
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

### Setup Environment - Shell/Terminal (Pipenv)
```
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run Streamlit Dashboard 
```
cd dashboard
streamlit run dashboard.py
```