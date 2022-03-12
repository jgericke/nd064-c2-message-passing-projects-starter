FROM node:14.8.0-alpine3.12
ENV SKIP_PREFLIGHT_CHECK=true
WORKDIR .

COPY package.json ./

RUN npm install
RUN npm install react-scripts@3.4.3 -g

CMD ["pwd"]
COPY . ./

EXPOSE 3000

CMD ["npm", "start"]

