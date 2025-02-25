#!/bin/bash
# Cria o ambiente se ele não existir
if ! conda env list | grep -q "graph-props"; then
    echo "Criando o ambiente conda 'graph-props'..."
    conda env create -f environment.yml
else
    echo "Ambiente 'graph-props' já existe."
fi

echo "Ativando o ambiente 'graph-props'..."
conda activate graph-props

echo "Executando o programa..."
python main.py
