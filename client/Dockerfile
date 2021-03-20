FROM node:12.18.2-alpine

COPY ./package.json /usr/src/app/
WORKDIR /usr/src/app
RUN npm install

COPY . /usr/src/app
COPY ./entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod 755 /usr/local/bin/entrypoint.sh

EXPOSE 8080


ENTRYPOINT [ "entrypoint.sh" ]
# DEBUG=falseの場合の実行コマンド
CMD npm run build-no-clean
