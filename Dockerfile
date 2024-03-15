FROM ghcr.io/typst/typst

RUN apk add python3

COPY \
	entrypoint.py \
	/root/

ENTRYPOINT ["python3", "/root/entry.py"]