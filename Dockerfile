# Use official slim Python image
FROM python:3.12-slim

# Install LaTeX and required fonts for matplotlib text rendering
RUN apt-get update && apt-get install -y --no-install-recommends \
    texlive-latex-base texlive-latex-recommended texlive-latex-extra texlive-science texlive-pictures \
    texlive-fonts-recommended texlive-fonts-extra ghostscript ps2eps latexmk && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

# Install remaining lightweight packages in a separate layer.
RUN apt-get update && apt-get install -y --no-install-recommends \
    fonts-lmodern dvipng cm-super fish git && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

# Keep a copy of the bundled requirements as a fallback
COPY requirements.txt /app/requirements.txt

# Install uv system-wide so it creates/uses the project-local .venv under /app
RUN pip install --no-cache-dir uv

# Create a non-root user (UID 1000) to run the application
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app && \
    chown -R appuser:appuser /app

# Add sane fish defaults for interactive shells
COPY fish_settings.fish /etc/fish/conf.d/fish_settings.fish
RUN sed -i 's/\r$//' /etc/fish/conf.d/fish_settings.fish && chmod 644 /etc/fish/conf.d/fish_settings.fish

# Default working directory inside container for mounted project (map your host dir to /app)
WORKDIR /app

# Restore standalone entrypoint script (do not inline)
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN sed -i 's/\r$//' /usr/local/bin/entrypoint.sh && chmod +x /usr/local/bin/entrypoint.sh

# Switch to non-root user
USER appuser

# Run the entrypoint script that performs uv sync and drops into fish
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
