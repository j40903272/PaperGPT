---
title: PaperGPT
app_file: src/app.py
sdk: gradio
sdk_version: 3.35.2
---
# PaperGPT
Paper editor tool


``` python 3.8
python -m pip install -r requirements.txt
cd src
python app.py
```


### deploy to huggingface space

```
python -m pip install huggingface_hub
huggingface-cli login
```

```
gradio deploy
```

```
setup space repository secret: OPENAI_API_KEY
```
