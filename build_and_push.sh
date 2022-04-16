docker build -t arkhoshghalb/codequest:worker . && docker push arkhoshghalb/codequest:worker

cd public_image
docker build -t arkhoshghalb/codequest:public_runner . && docker push arkhoshghalb/codequest:public_runner
cd ..