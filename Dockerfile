# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy only required files first (to leverage Docker cache)
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose ports if necessary (uncomment and set the correct port)
# EXPOSE 8000

# Set environment variables (optional, but recommended to pass at runtime)
# ENV OPENAI_API_KEY=your_openai_api_key
# ENV TWITTER_API_KEY=your_twitter_api_key
# ...

# Specify the command to run on container start
CMD ["python", "bots/run_xbot.py", "--config_path=config/xbot_character.json", "--table_name=xbot_data"]