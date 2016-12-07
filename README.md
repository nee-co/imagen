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

#### Docker

```bash
git clone https://github.com/naoki912/imagen.git
cd imagen/
docker build --tag=imagen --no-cache .
docker run -d -p 8000:8000 imagen
```
