kubectl delete -f nosso.yaml
docker build  -t nosso-flask:latest .
docker tag   nosso-flask:latest sjc.ocir.io/oraclepartnersas/nosso-flask:latest
docker push  sjc.ocir.io/oraclepartnersas/nosso-flask:latest
#change ords.yaml
kubectl create -f nosso.yaml
sleep 20
kubectl get all
