module load python/3.6
ENVDIR=/tmp/$RANDOM
virtualenv --no-download $ENVDIR
source $ENVDIR/bin/activate
pip install --no-index --upgrade pip
pip install --no-index numpy
pip install --no-index scikit-image
pip install --no-index imageio
pip install --no-index scipy
pip freeze > requirements.txt
deactivate
rm -rf $ENVDIR