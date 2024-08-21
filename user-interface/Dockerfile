# compile
FROM node:16.16.0-alpine as deps
RUN apk add --no-cache libc6-compat
WORKDIR /frontend
COPY package.json yarn.lock ./
RUN yarn install --only=production --frozen-lockfile

FROM node:16.16.0-alpine AS builder
WORKDIR /frontend
COPY . .
COPY --from=deps /frontend/node_modules ./node_modules
RUN yarn build

# production
FROM node:16.16.0-alpine as production-stage
WORKDIR /frontend
COPY --from=builder /frontend .
RUN apk add --no-cache make
RUN chmod +x start.sh

CMD ["sh", "./start.sh"]