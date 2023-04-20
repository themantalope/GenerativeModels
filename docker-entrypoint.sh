
#!/usr/bin/env bash
nohup jupyter-lab --port 8888 --ip="*" --allow-root --NotebookApp.token='' --NotebookApp.password='' &

until [ -f nohup.out ]
do
     sleep 1
done

cat nohup.out

/bin/bash
