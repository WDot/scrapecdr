FROM node:16-alpine

# Check https://github.com/nodejs/docker-node/tree/b4117f9333da4138b03a546ec926ef50a31506c3#nodealpine to understand why libc6-compat might be needed.
RUN apk add --update --no-cache bind-tools
RUN apk add --no-cache libc6-compat

WORKDIR /app/

#UGLY HACK

# If using npm with a `package-lock.json` comment out above and use below instead
COPY package.json package-lock.json ./ 

COPY . .

RUN export TMPDIR="/tmp"

RUN npm ci

RUN npm run build

# Uncomment the following line in case you want to disable telemetry during runtime.
# ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# You only need to copy next.config.js if you are NOT using the default configuration
#COPY --from=builder /app/next.config.js ./

#USER nextjs

EXPOSE 3000

CMD npm run dev
