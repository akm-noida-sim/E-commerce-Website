# Deployment

1. Create a MongoDB Atlas cluster and database user; set `MONGO_URI` to its TLS connection string.
2. Deploy `backend` to Render as a Python web service. Build command: `pip install -r requirements.txt`; start command: `gunicorn --chdir backend run:app`. Add `SECRET_KEY`, `JWT_SECRET_KEY`, `MONGO_URI`, `CLIENT_ORIGIN`, and `FLASK_ENV=production`.
3. Deploy `frontend` to Vercel with root directory `frontend`, build command `npm run build`, output directory `dist`, and environment variable `VITE_API_URL=https://YOUR-RENDER-SERVICE.onrender.com/api`.
4. Set the Render `CLIENT_ORIGIN` to the exact Vercel URL and redeploy. Use long random secrets and Atlas network rules appropriate to Render.

Before launch, create a least-privilege admin user, exercise checkout against a test product, and configure a custom domain/HTTPS.
