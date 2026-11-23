#!/bin/bash

# Aktywacja środowiska wirtualnego
source venv/bin/activate 2>/dev/null || source .venv/bin/activate 2>/dev/null || true

# Wybór odpowiedniej wersji Pythona
PYTHON_CMD="python3.11"
if ! command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3"
fi

PACKAGE_PATH="papers.manipulation_of_hamming.experiments_enhanced"

# Zamień kropki w ścieżce pakietu na ukośniki (powstanie: papers/manipulation_of_hamming/experiments_enhanced)
DIR_PATH=$(echo "$PACKAGE_PATH" | tr '.' '/')

# Sprawdź, czy ten katalog istnieje
if [ ! -d "$DIR_PATH" ]; then
    echo "BŁĄD: Katalog $DIR_PATH nie istnieje!"
    exit 1
fi

# Szukaj plików plot_*.py bezpośrednio w tym folderze
files=("$DIR_PATH"/plot_*.py)
if [ ! -e "${files[0]}" ]; then
    echo "BŁĄD: Nie znaleziono żadnych plików plot_*.py w folderze $DIR_PATH!"
    exit 1
fi

# Iteracja po plikach w tamtym folderze
for file in "$DIR_PATH"/plot_*.py; do
    if [ -f "$file" ]; then
        module_name=$(basename "$file" .py)
        full_module="${PACKAGE_PATH}.${module_name}"
        
        echo "--------------------------------------------------"
        echo "Uruchamiam moduł: $full_module"
        echo "--------------------------------------------------"
        
        # Uruchomienie jako moduł z głównego katalogu projektu
        $PYTHON_CMD -m "$full_module" "$@"
        
        exit_code=$?
        if [ $exit_code -ne 0 ]; then
            echo "-> BŁĄD: Moduł $full_module zakończył się błędem (kod: $exit_code)."
        fi
    fi
done

# Dezaktywacja środowiska
deactivate 2>/dev/null || true