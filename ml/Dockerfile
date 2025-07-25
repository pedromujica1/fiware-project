FROM python:3.12

WORKDIR /ml
#copia tudo
COPY . .

# 1. Instala pip e limpa instalações prévias do NumPy
RUN pip install --upgrade pip && \
    pip uninstall -y numpy && \
    rm -rf /root/.cache/pip

# 2. Instala o NumPy com versão fixa ANTES de outras dependências
RUN pip install --no-cache-dir numpy==1.26.0

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copia o modelo e o código
COPY RF_Regressor.joblib .
COPY app ./app


EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]