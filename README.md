# Article insight bot

This is a bot insight for articles. It uses the [Hugging Face](https://huggingface.co/) model to generate insights for articles.

## Docker
```bash
docker build -f Dockerfile -t article_insight_bot_image .
```

```bash
sudo docker run -it -d --env-file .env --restart unless-stopped  -v /{full path to project}/logs/:/app/logs/ --name article_insight_bot article_insight_bot_image
```