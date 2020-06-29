#/bin/bash
echo "\033[36m ______                    "
echo "|___  /                    "
echo "   / / _   _   __ _   ___  "
echo "  / / | | | | / _\` | / _ \ "
echo " / /__| |_| || (_| || (_) |"
echo "/_____|\__, | \__, | \___/ "
echo "        __/ |  __/ |       "
echo "       |___/  |___/        \033[0m\n\n"


echo "\033[32m Building image tag...\033[0m 🏷\n"
SHORT_HASH=$(git rev-parse --short HEAD)
IMAGE_TAG="gcr.io/gfrog-commerce/chatbot:${SHORT_HASH}"

echo "\033[32m Building image...\033[0m 🛠\n"
docker build -t $IMAGE_TAG .

echo "\033[32m Pushing image...\033[0m ⬆️\n"
docker push $IMAGE_TAG

echo "\033[32m Deploying to google cloud...\033[0m 🚀\n"
gcloud run deploy chatbot --image $IMAGE_TAG --platform managed --allow-unauthenticated