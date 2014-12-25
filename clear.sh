find . -name "*.pyc" -exec echo 'del ' {} \; -exec rm -f {} \;
