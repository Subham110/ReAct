# ==============================================================================
# STAGE 1: Builder (Compiles React 19 SPA with Node)
# ==============================================================================
FROM node:22-alpine AS builder

WORKDIR /app

# Install npm dependencies first (utilizes Docker layer caching)
COPY package.json package-lock.json* ./
RUN npm ci --prefer-offline --no-audit

# Copy source code and build production assets
COPY . .
RUN npm run build

# ==============================================================================
# STAGE 2: Clean Production Web Server & Reverse Proxy
# ==============================================================================
FROM nginx:alpine-slim AS runner

# Remove default nginx static files
RUN rm -rf /usr/share/nginx/html/*

# Copy compiled distribution from builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom reverse proxy & load balancer configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

# Healthcheck testing frontend Nginx availability
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
