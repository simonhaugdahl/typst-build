FROM ghcr.io/typst/typst

RUN apk add python3

COPY \
	entry.py \
	/root/

ENTRYPOINT ["python3", "/root/entry.py"]