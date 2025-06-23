# Copyright (c) 2025 Privacy Guardian Agents by Privacy License . All rights reserved.
# Licensed under the MIT License modified with the Commons Clause.
# For complete license terms, see https://gitlab.com/tnabanitade/privacysdk/-/blob/master/LICENSE
# Commercial use is prohibited without a license.
# Contact for Commercial License: nabanita@privacylicense.com | https://privacylicense.ai

# Use the official Node.js runtime as the base image
FROM node:20-slim

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json (if available)
COPY package*.json ./

# Install all dependencies (including dev dependencies for building)
RUN npm ci

# Copy the rest of the application code
COPY . .

# Build the TypeScript application
RUN npm run build:prod

# Remove dev dependencies to keep the image lean
RUN npm prune --production

# Create a non-root user to run the application
RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose the port the app runs on
EXPOSE 8080

# Set environment variables
ENV NODE_ENV=production
ENV PORT=8080

# Start the application
CMD ["node", "dist/web/server.js"] 