# compile
FROM node:16.16.0-alpine as deps
RUN apk add --no-cache libc6-compat
WORKDIR /src
COPY package.json yarn.lock ./
RUN yarn install --only=production --frozen-lockfile

FROM node:16.16.0-alpine AS builder
WORKDIR /src
COPY . .
COPY --from=deps /src/node_modules ./node_modules
RUN yarn build

# production
FROM node:16.16.0-alpine as production-stage
WORKDIR /crimeradar-ui
COPY --from=builder /src .

RUN yarn account

EXPOSE 3000

CMD [ "node", "index.js" ]