# Nee-co Imagen

### install & usage

```bash
git clone https://github.com/naoki912/imagen.git
pip install -r imagen/imagen/requirements.freeze
pip install gunicorn
cd imagen/
export PYTHONPATH=`pwd`
cd imagen/
gunicorn -b 0.0.0.0:8000 app:app
```
